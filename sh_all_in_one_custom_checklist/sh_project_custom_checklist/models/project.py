# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    project_complete_state = fields.Selection([("completed", "Completed"),
                                               ("cancelled", "Cancelled")],
                                              compute="_compute_complete_check",
                                              string="State",
                                              readonly=True,
                                              index=True,
                                              search="_search_state")

    def _search_state(self, operator, value):
        if operator in ["="]:
            # In case we search against anything else than new, we have to invert the operator
            complete_so_list = []
            incomplete_so_list = []

            for rec in self.search([]):
                total_cnt = self.env[
                    "project.custom.checklist.line"].search_count([
                        ("project_id", "=", rec.id)
                    ])
                compl_cnt = self.env[
                    "project.custom.checklist.line"].search_count([
                        ("project_id", "=", rec.id), ("state", "=", "completed")
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
            return [("id", "in", complete_so_list)]
        else:
            return [("id", "in", incomplete_so_list)]

    @api.depends("custom_checklist_ids")
    def _compute_custom_checklist(self):
        for rec in self:
            total_cnt = self.env["project.custom.checklist.line"].search_count(
                [("project_id", "=", rec.id),])
            compl_cnt = self.env["project.custom.checklist.line"].search_count(
                [("project_id", "=", rec.id), ("state", "=", "completed")])

            if total_cnt > 0:
                rec.custom_checklist = (100.0 * compl_cnt) / total_cnt
            else:
                rec.custom_checklist = 0

    @api.depends("custom_checklist")
    def _compute_complete_check(self):
        if self:
            for data in self:
                if data.custom_checklist >= 100:
                    data.project_complete_state = "completed"
                else:
                    data.project_complete_state = "cancelled"

    custom_checklist_ids = fields.One2many("project.custom.checklist.line",
                                           "project_id", "Checklist", copy=True)
    custom_checklist = fields.Float("Checklist Completed",
                                    compute="_compute_custom_checklist", digits=(12, 0))

    checklist_template_ids = fields.Many2many("project.custom.checklist.template",
                                              string="Checklist Template", check_company=True)

    @api.onchange('checklist_template_ids')
    def onchange_checklsit_template(self):
        update_ids = []
        for i in self.checklist_template_ids:
            for j in i._origin.checklist_template_ids:
                new_id = self.env["project.custom.checklist.line"].create({
                    'name':
                    j.id,
                    'description':
                    j.description
                })
                update_ids.append(new_id.id)

        self.custom_checklist_ids = [(6, 0, update_ids)]
