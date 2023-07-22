# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    complete_state = fields.Selection([('completed', 'Completed'),
                                       ('cancelled', 'Cancelled')],
                                      compute="_complete_check",
                                      string="State",
                                      readonly=True,
                                      index=True,
                                      search="_search_state")

    def _search_state(self, operator, value):

        if operator in ['=']:
            # In case we search against anything else than new, we have to invert the operator
            complete_so_list = []
            incomplete_so_list = []

            for rec in self.search([]):
                total_cnt = self.env[
                    'product.template.custom.checklist.line'].search_count([
                        ('sh_product_template_id', '=', rec.id)
                    ])
                compl_cnt = self.env[
                    'product.template.custom.checklist.line'].search_count([
                        ('sh_product_template_id', '=',
                         rec.id), ('state', '=', 'completed')
                    ])

                if total_cnt > 0:
                    rec.custom_checklist = (100.0 * compl_cnt) / total_cnt
                    if rec.custom_checklist == 100:
                        complete_so_list.append(rec.id)
                    else:
                        incomplete_so_list.append(rec.id)
                else:
                    incomplete_so_list.append(rec.id)

        if value == True:
            return [('id', 'in', complete_so_list)]
        else:
            return [('id', 'in', incomplete_so_list)]

    @api.depends('custom_checklist_ids')
    def _compute_custom_checklist(self):
        if self:
            for rec in self:
                total_cnt = self.env[
                    'product.template.custom.checklist.line'].search_count([
                        ('sh_product_template_id', '=', rec.id)
                    ])
                compl_cnt = self.env[
                    'product.template.custom.checklist.line'].search_count([
                        ('sh_product_template_id', '=',
                         rec.id), ('state', '=', 'completed')
                    ])

                if total_cnt > 0:
                    rec.custom_checklist = (100.0 * compl_cnt) / total_cnt
                else:
                    rec.custom_checklist = 0

    @api.depends('custom_checklist')
    def _complete_check(self):
        if self:
            for data in self:
                if data.custom_checklist >= 100:
                    data.complete_state = 'completed'
                else:
                    data.complete_state = 'cancelled'

    custom_checklist_ids = fields.One2many("product.template.custom.checklist.line",
                                           "sh_product_template_id", "Checklist")
    custom_checklist = fields.Float("Checklist Completed",
                                    compute="_compute_custom_checklist", index=True, digits=(12, 0))

    custom_checklist_template_ids = fields.Many2many(
        'product.custom.checklist.template', check_company=True)

    @api.onchange('custom_checklist_template_ids')
    def onchange_custom_checklist_template_ids(self):
        update_ids = []
        for i in self.custom_checklist_template_ids:
            for j in i._origin.sh_checklist_template_ids:
                new_id = self.env["product.template.custom.checklist.line"].create({
                    'name':
                    j.id,
                    'description':
                    j.description
                })
                update_ids.append(new_id.id)

        self.custom_checklist_ids = [(6, 0, update_ids)]
