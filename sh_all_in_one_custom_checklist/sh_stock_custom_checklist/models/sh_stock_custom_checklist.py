# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api


class StockCustomChecklist(models.Model):
    _name = "stock.custom.checklist"
    _description = "Stock Custom Checklist"
    _order = 'sequence,name, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    description = fields.Char()
    company_id = fields.Many2one("res.company",
                                 string="Company",
                                 default=lambda self: self.env.company)


class StockCustomChecklistLine(models.Model):
    _name = "stock.custom.checklist.line"
    _description = "Stock Custom Checklist Line"
    _order = "id desc"

    name = fields.Many2one("stock.custom.checklist",
                           required=True, check_company=True)
    description = fields.Char()
    updated_date = fields.Date("Date",
                               readonly=True,
                               default=fields.Datetime.now())
    state = fields.Selection([("new", "New"), ("completed", "Completed"),
                              ("cancelled", "Cancelled")],
                             default="new",
                             readonly=True,
                             index=True)

    stock_id = fields.Many2one("stock.picking")
    company_id = fields.Many2one(
        related='stock_id.company_id',
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
