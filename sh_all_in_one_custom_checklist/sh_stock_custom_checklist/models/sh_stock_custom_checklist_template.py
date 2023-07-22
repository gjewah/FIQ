# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class StockCustomChecklist(models.Model):
    _name = "stock.custom.checklist.template"
    _description = "Stock Custom Checklist Template"
    _order = 'sequence,name, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    checklist_template_ids = fields.Many2many(
        comodel_name='stock.custom.checklist',
        relation='checklist_template_table',
        string='CheckList Template', check_company=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company)
