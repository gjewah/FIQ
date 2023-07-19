#coding: utf-8

from odoo import _, fields, models


class res_config_settings(models.TransientModel):
    """
    Overwrite to add numbering settings
    """
    _inherit = "res.config.settings"

    group_task_numbers_from_project = fields.Boolean(
        string="Project code in task reference numbers",
        implied_group="task_numbers.group_task_numbers_from_project",
        group="base.group_portal,base.group_user,base.group_public",
    )

    def action_update_all_task_numbers(self):
        """
        The method to update numbers of all tasks

        Methods:
         * action_update_numbering of project.task
        """
        task_ids = self.env["project.task"].search([])
        task_ids.action_update_numbering()

    def action_open_ir_task_sequence(self):
        """
        The method to open ir.sequence
        """
        seq_id = self.env["ir.sequence"].search([("code", "=", "project.task")], limit=1)
        if seq_id:
            return {
                "res_id": seq_id.id,
                "name": _("Task Numbering"),
                "type": "ir.actions.act_window",
                "res_model": "ir.sequence",
                "view_mode": "form",
                "target": "new",
            }