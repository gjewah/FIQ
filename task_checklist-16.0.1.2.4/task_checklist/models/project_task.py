#coding: utf-8

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

INTER_WARNING = _(u"The task '{}' cannot be moved to the stage '{}'. The stage(s) [{}] cannot be skipped!")
REGRESS_WARNING = _(u"The task '{}' cannot be moved back to stage '{}'. This stage does not allow regression!")
STAGEVALIDATIONERRORMESSAGE = _(u"""Please enter the checklist for the task '{0}'!
You can't move the task forward until you confirm all jobs have been done on the stage '{1}'. Not done checkpoints:
 * {2}""")

def InternalUserCheck(method):
    """
    The decorator used to check the user for being internal
    Not internal users are not assumed to work or be restricted by checklists
    """
    def wrapper(self, *args, **kwargs):
        if self.env.user.has_group("base.group_user"):
            return method(self, *args, **kwargs)
        else:
            return True
    return wrapper

def SuperRightsCheck(method):
    """
    The decorator used to check the user for beeing a superuser
    Superusers are not assumed to be restricted by checklists
    """
    def wrapper(self, *args, **kwargs):
        """
        The wrapper method itself that is designed to check the user for being internal
        """
        if self.env.user.has_group("task_checklist.group_task_checklist_superuser") or self.env.su:
            return True
        else:
            return method(self, *args, **kwargs)
    return wrapper


class project_task(models.Model):
    """
    Re-write to add checklist mechanics
    """
    _inherit = "project.task"

    @api.depends(
        "stage_id", "stage_id.default_check_list_ids", "stage_id.default_check_list_ids.project_task_type_id",
        "check_list_line_ids", "check_list_line_ids.project_task_type_id")
    def _compute_check_list_len(self):
        """
        Compute method for 'check_list_len' & 'checklist_progress'

        Methods:
         * _get_filtered of check.list
        """
        for task_id in self:
            stage_id = task_id.stage_id
            default_check_list_ids = stage_id and stage_id.default_check_list_ids._get_filtered(stage_id) \
                or self.env["check.list"]
            check_list_len = len(default_check_list_ids)
            check_list_line_ids = task_id.check_list_line_ids._get_filtered(stage_id)
            task_id.check_list_len = check_list_len
            task_id.checklist_progress = check_list_len and (len(check_list_line_ids) / check_list_len) * 100 or 0.0

    check_list_line_ids = fields.Many2many(
        "check.list",
        "project_task_check_list_rel_table",
        "project_task_id",
        "check_list_id",
        string="Checklist",
        help="Confirm that you finished all the points. Otherwise, you will not be able to move the task forward",
        copy=False,
    )
    check_list_history_ids = fields.One2many("check.history", "task_id", string="History", copy=False)
    check_list_len = fields.Integer(string="Total points", compute=_compute_check_list_len, store=True, copy=False)
    checklist_progress = fields.Float(
        string="Checklist progress",
        compute=_compute_check_list_len,
        store=True,
        copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Overwrite to check whether the check list is pre-filled and check whether this user might do that
         1. Simulate create with a default stage and no chekpoints
          1.1. Replace currently written stage with the default one
          1.2. Remove check list item, so they will be written afterwards
         2. For each task, write actual stage and checkpoints. Thus, consider transfer default stage > new stage with
            done checkpoints

        Methods:
         * _get_default_stage_id (note: it returns Int)
        """
        # 1
        new_vals_list = []
        for vals in vals_list:
            new_values = {}
            # 1.1
            if vals.get("stage_id"):
                default_stage_id = self._get_default_stage_id()
                if default_stage_id and vals.get("stage_id") != default_stage_id:
                    new_values.update({"stage_id": vals.get("stage_id")})
                    vals.update({"stage_id": default_stage_id})
            # 1.2
            if vals.get("check_list_line_ids"):
                new_values.update({"check_list_line_ids": vals.get("check_list_line_ids")})
                vals.pop("check_list_line_ids")
            new_vals_list.append(new_values)
        task_ids = super(project_task, self).create(vals_list)
        # 2
        for itera in range(0, len(task_ids)):
            new_vals = new_vals_list[itera]
            if new_vals:
                task_ids[itera].write(new_vals)
        return task_ids

    def write(self, vals):
        """
        Overwrite to:
         1. Check rights to change checklist
         2. Register history
         3. Make sure forbidden regress is not undertaken
         4. Check completeness of check points
         5. Delete items that should not be kept for further use

        Methods:
         * _check_rights_and_register_history
         * _check_regress_possible
         * _check_checklist_complete
         * _save_checkitems
        """
        new_checkpoint_ids = None
        if vals.get("check_list_line_ids") is not None and not self.env.context.get("automatic_checks"):
            new_checkpoint_ids = self.env["check.list"].browse(vals.get("check_list_line_ids")[0][2])
            self._check_rights_and_register_history(new_checkpoint_ids)
        if vals.get("stage_id"):
            if vals.get("check_list_line_ids") is not None:
                vals.pop("check_list_line_ids") # will be updated in '_save_checkitems'
            new_stage_id = self.env["project.task.type"].browse(vals.get("stage_id"))
            new_project_id = vals.get("project_id")
            self._check_regress_possible(new_stage_id)
            self._check_skipping(new_stage_id, new_project_id)
            self._check_checklist_complete(new_stage_id, new_checkpoint_ids)
            self._save_checkitems(new_stage_id, new_checkpoint_ids)
        return super(project_task, self).write(vals)

    @InternalUserCheck
    def _check_rights_and_register_history(self, new_check_line_ids):
        """
        The method to get the changes in the checklist and:
         1. Check whether the user can make those changes based on the checkpoint settings
         2. Register done checks and unchecks

        Methods:
         * action_check_cheklist_rights of check.list

        Args:
         * new_check_line_ids - check.list recordset

        Returns:
         *  check.history recordset or True
        """
        history_vals_list = []
        for task in self:
            old_check_line_ids = task.check_list_line_ids
            to_add_items = (new_check_line_ids - old_check_line_ids)
            to_remove_items = (old_check_line_ids - new_check_line_ids)
            changed_items = to_add_items | to_remove_items
            changed_items.action_check_cheklist_rights()
            history_vals_list += [
                {"task_id": task.id, "check_list_id": item.id, "done_action": "done"} for item in to_add_items
            ]
            history_vals_list += [
                {"task_id": task.id, "check_list_id": item.id, "done_action": "reset"} for item in to_remove_items
            ]
        return history_vals_list and self.env["check.history"].create(history_vals_list) or True

    @InternalUserCheck
    @SuperRightsCheck
    def _check_regress_possible(self, new_stage_id):
        """
        The method to check whether it is regress, and if yes whether the stage allows that

        Args:
         * new_stage_id - project.task.type object
        """
        if new_stage_id.forbid_back_progress:
            for task in self:
                if new_stage_id.sequence < task.stage_id.sequence:
                    raise ValidationError(REGRESS_WARNING.format(task.name, new_stage_id.name))
        return True

    @InternalUserCheck
    @SuperRightsCheck
    def _check_skipping(self, new_stage_id, new_project_id):
        """
        The method to check whether it any stage is skipped, and if yes to define whether any of those might be skipped

        Args:
         * new_stage_id - crm.stage record
         * new_project_id - int or False or None
        """
        if new_stage_id.no_need_for_checklist:
            return True
        domain = [
            ("cannot_be_missed", "=", True), ("sequence", "<", new_stage_id.sequence), ("id", "!=", new_stage_id.id),
        ]
        for task in self:
            if new_stage_id.sequence <= task.stage_id.sequence:
                return True
            if new_project_id is not None:
                project_id = new_project_id and new_project_id.id or False
            else:
                project_id = task.project_id.id
            domain.extend([
                ("id", "!=", task.stage_id.id), ("sequence", ">", task.stage_id.sequence),
                ("project_ids", "in", project_id),
            ])
            inter_stage_ids = self.env["project.task.type"].search(domain)
            if inter_stage_ids:
                raise ValidationError(INTER_WARNING.format(
                    task.name, new_stage_id.name, ", ".join(inter_stage_ids.mapped("name")))
                )
        return True

    @InternalUserCheck
    @SuperRightsCheck
    def _check_checklist_complete(self, new_stage_id, new_checkpoint_ids):
        """
        The method to make sure checklist is filled in case of task progress

        Args:
         * new_stage_id - project.task.type object
         * new_checkpoint_ids - check.list recordset or False

        Methods:
         * _get_filtered of check.list
        """
        for task in self:
            prev_stage_id = task.stage_id
            if prev_stage_id == new_stage_id or new_stage_id.sequence < prev_stage_id.sequence \
                    or new_stage_id.no_need_for_checklist:
                continue
            if new_checkpoint_ids is None:
                new_checkpoint_ids = task.check_list_line_ids
            done_checkpoints = new_checkpoint_ids._get_filtered(prev_stage_id)
            needed_checkpoints = prev_stage_id.default_check_list_ids._get_filtered(prev_stage_id)
            not_done_checkpoints = needed_checkpoints - done_checkpoints
            if not_done_checkpoints:
                twarning = "\n * ".join(not_done_checkpoints.mapped("name"))
                raise ValidationError(STAGEVALIDATIONERRORMESSAGE.format(task.name, prev_stage_id.name, twarning))
        return True

    def _save_checkitems(self, new_stage_id, new_checkpoint_ids):
        """
        The method to clear all items that relate to the previous stage but that are marked as not saved
        We keep all items for the current stage disregarding whether they should be saved or not

        Args:
         * stage_id - project.task.type object
         * new_checkpoint_ids - check.list recordset or False

        Returns:
         * dict - new vals to update
        """
        for task in self:
            if new_checkpoint_ids is None:
                new_checkpoint_ids = task.check_list_line_ids
            updated_checkpoint_ids = new_checkpoint_ids.filtered(
                lambda item: not item.should_be_reset or item.project_task_type_id == new_stage_id
            )
            task.with_context(automatic_checks=True).check_list_line_ids = [(6, 0, updated_checkpoint_ids.ids)]
