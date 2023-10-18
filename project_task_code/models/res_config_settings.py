# Copyright 2023 Abraham Anes <abrahamanes@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    project_task_unique_code = fields.Boolean(
        string="Unique Task Code",
        config_parameter="project_task_code.project_task_unique_code",
        default=False,
    )
