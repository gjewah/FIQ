# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api


class ProjectCustomChecklist(models.Model):
    _name = "project.custom.checklist"
    _description = "Project Custom Checklist"
    _order = 'sequence,name, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    description = fields.Char()
    company_id = fields.Many2one("res.company",
                                 string="Company",
                                 default=lambda self: self.env.company)


class ProjectCustomChecklistLine(models.Model):
    _name = "project.custom.checklist.line"
    _description = "Project Custom Checklist Line"
    _order = "id desc"

    name = fields.Many2one("project.custom.checklist", required=True)
    description = fields.Char()
    updated_date = fields.Date("Date",
                               readonly=True,
                               default=fields.Datetime.now())
    state = fields.Selection([("new", "New"), ("completed", "Completed"),
                              ("cancelled", "Cancelled")],
                             default="new",
                             readonly=True,
                             index=True)

    project_id = fields.Many2one("project.project")
    company_id = fields.Many2one(
        related='project_id.company_id',
        store=True,)

    def btn_check(self):
        for rec in self:
            rec.write({"state": "completed"})

    def btn_close(self):
        for rec in self:
            rec.write({"state": "cancelled"})

    @api.onchange("name")
    def onchange_custom_chacklist_name(self):
        self.description = self.name.description
