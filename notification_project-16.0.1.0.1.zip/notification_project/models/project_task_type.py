# -*- coding: utf-8 -*-

from odoo import fields, models


class project_task_type(models.Model):
    """
    Override to add setting of which tasks should be notified
    """
    _inherit = "project.task.type"

    is_notify = fields.Boolean(
        "Send notification",
        default=False,
        help="Tasks on this stage will be included in daily reminders",
    )
