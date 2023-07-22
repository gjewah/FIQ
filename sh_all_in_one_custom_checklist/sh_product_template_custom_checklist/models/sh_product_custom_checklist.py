# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api


class ProductCustomChecklist(models.Model):
    _name = "product.custom.checklist"
    _description = 'Product Custom Checklist'

    name = fields.Char(required=True)
    description = fields.Char()
    company_id = fields.Many2one("res.company",
                                 string="Company",
                                 default=lambda self: self.env.company)


class ProductTemplateCustomChecklistLine(models.Model):
    _name = "product.template.custom.checklist.line"
    _description = 'Product Template Custom Checklist Line'

    name = fields.Many2one("product.custom.checklist",
                           required=True, check_company=True)
    description = fields.Char()
    updated_date = fields.Date("Date",
                               readonly=True,
                               default=fields.Datetime.now())
    state = fields.Selection([('new', 'New'), ('completed', 'Completed'),
                              ('cancelled', 'Cancelled')],
                             default='new',
                             readonly=True,
                             index=True)

    sh_product_template_id = fields.Many2one("product.template")
    company_id = fields.Many2one(
        related='sh_product_template_id.company_id',
        store=True,)

    def btn_check(self):
        for rec in self:
            rec.write({'state': 'completed'})

    def btn_close(self):
        for rec in self:
            rec.write({'state': 'cancelled'})

    @api.onchange('name')
    def onchange_custom_chacklist_name(self):
        self.description = self.name.description
