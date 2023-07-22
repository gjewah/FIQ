# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class MRPCustomChecklistTemplate(models.Model):
    _name = "mrp.custom.checklist.template"
    _description = 'MRP Custom Checklist Template'
    _order = 'sequence,name, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    checklist_template_ids = fields.Many2many('mrp.custom.checklist',
                                              string="Check List", check_company=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company)
