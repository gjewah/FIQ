# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class SaleCustomChecklistTemplate(models.Model):
    _name = "sale.custom.checklist.template"
    _description = "Sale Custom Checklist Template"
    _order = 'sequence,name, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    checklist_template = fields.Many2many('sale.custom.checklist',
                                          string="Check List", check_company=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company)
