# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class ProductCustomChecklistTemplate(models.Model):
    _name = "product.custom.checklist.template"
    _description = "Product Custom Checklist Template"

    name = fields.Char(required=True)
    sh_checklist_template_ids = fields.Many2many(
        comodel_name='product.custom.checklist',
        relation='product_checklist_template_table',
        string='CheckList Template', check_company=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company)
