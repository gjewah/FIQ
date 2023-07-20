#coding: utf-8

from odoo import fields, models


class project_task_type(models.Model):
    """
    Overwrite to add checklist and checklist settings
    """
    _inherit = "project.task.type"

    default_check_list_ids = fields.One2many("check.list", "project_task_type_id", string="Checklist")
    no_need_for_checklist = fields.Boolean(
        string="No need for checklist",
        help="If checked, when you move a task TO this stage, no checklist is required (e.g. for 'Cancelled')"
    )
    cannot_be_missed = fields.Boolean(
        string="Forbid skipping this stage",
        help="If checked, this stage cannot be skipped if a task is moved further. The setting does not influence \
'No need for checklist' progress."
    )
    forbid_back_progress = fields.Boolean(
        string="Forbid regression to this stage",
        help="If checked, moving a task back TO this stage from further stages will be impossible",
    )
