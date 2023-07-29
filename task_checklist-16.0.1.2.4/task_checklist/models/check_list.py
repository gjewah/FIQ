#coding: utf-8

from odoo import _, fields, models
from odoo.exceptions import AccessError
from ..models.project_task import SuperRightsCheck

ACESSERRORMESSAGE = _(u"Sorry, but you don't have the right to confirm/disapprove '{0}'! \
Please contact your system administrator for assistance.")


class check_list(models.Model):
    """
    The model to keep check list items
    """
    _name = "check.list"
    _description = "Check List"

    name = fields.Char(string="What should be done on this stage", required=True)
    description = fields.Text(string="Notes")
    project_task_type_id = fields.Many2one("project.task.type", string="Task Stage", required=True)
    group_ids = fields.Many2many(
        "res.groups",
        "res_groups_check_list_rel_table",
        "res_groups_id",
        "check_list_id",
        string="User groups",
        help="Only users of those groups will be able to approve this checkpoint. Leave it empty if any user may \
confirm this item"
    )
    should_be_reset = fields.Boolean(
        string="Not saved",
        help="If checked each time a task is reset back to this stage, this checkpoint should be confirmed \
disregarding whether it has been confirmed before",
    )
    sequence = fields.Integer(string="Sequence")

    _order = "sequence, id"

    @SuperRightsCheck
    def action_check_cheklist_rights(self):
        """
        The method to check rights to fill check list item
        """
        for item in self:
            if item.group_ids and not (self.env.user.groups_id & item.group_ids):
                raise AccessError(ACESSERRORMESSAGE.format(item.name))
        return True

    def _get_filtered(self, stage_id):
        """
        The method to make sure checkpoint relates to the exact stage and team

        Args:
         * stage_id - project.task.type object

        Returns:
         * project.task.type recordset
        """
        final_checkpoint_ids = self.env["check.list"]
        if self:
            for item in self:
                if item.project_task_type_id == stage_id:
                    final_checkpoint_ids += item
        return final_checkpoint_ids
