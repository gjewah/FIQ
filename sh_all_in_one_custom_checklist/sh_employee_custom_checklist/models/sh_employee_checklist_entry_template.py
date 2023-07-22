# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class EmployeeEntryCustomChecklist(models.Model):
    _name = "employee.entry.custom.checklist.template"
    _description = "Employee Entry Custom Checklist Template"
    _order = 'sequence,name, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    entry_checklist_template = fields.Many2many(
        'employee.entry.custom.checklist',
        relation='employee_entry_checklist_template_table',
        string='Check List', check_company=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company)
