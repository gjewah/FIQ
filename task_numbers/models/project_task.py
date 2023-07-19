#coding: utf-8

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class project_task(models.Model):
    """
    Overwritting to implement tasks auto numbering
    """
    _inherit = "project.task"

    @api.depends("project_id.un_reference", "un_reference_short")
    def _compute_un_reference(self):
        """
        Compute method for un_reference
        """
        enable_pr_code = self.env.user.has_group("task_numbers.group_task_numbers_from_project")
        for task in self:
            if enable_pr_code and task.project_id.un_reference:
                task.un_reference = "{}/{}".format(task.project_id.un_reference, task.un_reference_short)
            else:
                task.un_reference = task.un_reference_short

    un_reference = fields.Char(string="Reference Number", compute=_compute_un_reference, store=True, compute_sudo=True)
    un_reference_short = fields.Char(string="Short Reference Number")

    @api.model_create_multi
    def create(self, vals_list):
        """
        Re-write to assign un_reference
        """
        for vals in vals_list:
            vals["un_reference_short"] = self.env["ir.sequence"].sudo().next_by_code("project.task")
        res = super(project_task, self).create(vals_list)
        return res

    def action_update_numbering(self):
        """
        The method to re-calculate current tasks number
        """
        for task in self:
            task.un_reference_short = self.env["ir.sequence"].sudo().next_by_code("project.task")

    @api.model
    def action_quick_search(self, search_key):
        """
        The method to search a task by auto number

        Args:
         * search_key - char to make a search
        """
        task_ids = self.search([("un_reference", "ilike", search_key)])
        action_id = False
        if len(task_ids) == 1:
            action_id = self.sudo().env.ref("task_numbers.project_task_action_only_form").read()[0]
            action_id["res_id"] = task_ids[0].id
        else:
            action_id = self.sudo().env.ref("project.project_task_action_from_partner").read()[0]
            action_id["context"] = {"search_default_un_reference": search_key}
            action_id["views"] = [(False, "kanban"), (False, "list"), (False, "form")]
        return action_id
