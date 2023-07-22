# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class CRMCustomChecklistTemplate(models.Model):
    _name = "crm.custom.checklist.template"
    _description = "CRM Custom Checklist Template"
    _order = 'sequence,name, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    checklist_template = fields.Many2many('crm.custom.checklist',
                                          string="Check List", check_company=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company)
