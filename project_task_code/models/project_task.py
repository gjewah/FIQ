# Copyright 2016 Tecnativa <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    code = fields.Char(
        string="Task Number",
        required=True,
        default="/",
        readonly=True,
        copy=False,
    )

    @api.constrains("code")
    def _check_project_task_unique_code(self):
        project_task_unique_code = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("project_task_code.project_task_unique_code")
        )

        if not project_task_unique_code:
            return

        for task in self:
            if self.search([("code", "=", task.code), ("id", "!=", task.id)], limit=1):
                raise ValidationError(_("The code must be unique!"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code", "/") == "/":
                vals["code"] = (
                    self.env["ir.sequence"].next_by_code("project.task") or "/"
                )
        return super().create(vals_list)

    def name_get(self):
        result = super().name_get()
        new_result = []

        for task in result:
            rec = self.browse(task[0])
            name = "[{}] {}".format(rec.code, task[1])
            new_result.append((rec.id, name))
        return new_result
