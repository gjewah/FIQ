# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @property
    def SELF_WRITABLE_FIELDS(self):
        result = super().SELF_WRITABLE_FIELDS
        result.update(["un_reference_short", "un_reference"])
        return result
