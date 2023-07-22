# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_entry_complete_state = fields.Selection([("completed", "Completed"),
                                                      ("cancelled", "Cancelled")],
                                                     compute="_compute_complete_check_entry",
                                                     string="Entry State",
                                                     readonly=True,
                                                     index=True,
                                                     search="_search_entry_state")

    def _search_entry_state(self, operator, value):
        if operator in ["="]:
            # In case we search against anything else than new, we have to invert the operator
            complete_so_list = []
            incomplete_so_list = []

            for rec in self.search([]):
                total_cnt = self.env[
                    "employee.entry.custom.checklist.line"].search_count([
                        ("employee_id", "=", rec.id)
                    ])
                compl_cnt = self.env[
                    "employee.entry.custom.checklist.line"].search_count([
                        ("employee_id", "=", rec.id), ("state", "=", "completed")
                    ])

                if total_cnt > 0:
                    rec.entry_custom_checklist = (
                        100.0 * compl_cnt) / total_cnt
                    if rec.entry_custom_checklist == 100:
                        complete_so_list.append(rec.id)
                    else:
                        incomplete_so_list.append(rec.id)
                else:
                    incomplete_so_list.append(rec.id)

        if value == True:
            return [("id", "in", complete_so_list)]
        else:
            return [("id", "in", incomplete_so_list)]

    @api.depends("entry_custom_checklist")
    def _compute_complete_check_entry(self):
        if self:
            for data in self:
                if data.entry_custom_checklist >= 100:
                    data.employee_entry_complete_state = "completed"
                else:
                    data.employee_entry_complete_state = "cancelled"

    employee_exit_complete_state = fields.Selection([("completed", "Completed"),
                                                     ("cancelled", "Cancelled")],
                                                    compute="_compute_complete_check_exit",
                                                    string="Exit State",
                                                    readonly=True,
                                                    index=True,
                                                    search="_search_exit_state")

    def _search_exit_state(self, operator, value):
        if operator in ["="]:
            # In case we search against anything else than new, we have to invert the operator
            complete_so_list = []
            incomplete_so_list = []

            for rec in self.search([]):
                total_cnt = self.env[
                    "employee.exit.custom.checklist.line"].search_count([
                        ("employee_id", "=", rec.id)
                    ])
                compl_cnt = self.env[
                    "employee.exit.custom.checklist.line"].search_count([
                        ("employee_id", "=", rec.id), ("state", "=", "completed")
                    ])

                if total_cnt > 0:
                    rec.entry_custom_checklist = (
                        100.0 * compl_cnt) / total_cnt
                    if rec.entry_custom_checklist == 100:
                        complete_so_list.append(rec.id)
                    else:
                        incomplete_so_list.append(rec.id)
                else:
                    incomplete_so_list.append(rec.id)

        if value == True:
            return [("id", "in", complete_so_list)]
        else:
            return [("id", "in", incomplete_so_list)]

    @api.depends("exit_custom_checklist")
    def _compute_complete_check_exit(self):
        if self:
            for data in self:
                if data.exit_custom_checklist >= 100:
                    data.employee_exit_complete_state = "completed"
                else:
                    data.employee_exit_complete_state = "cancelled"

    entry_custom_checklist_ids = fields.Many2many(
        "employee.entry.custom.checklist", string="Entry Checklist")
    exit_custom_checklist_ids = fields.Many2many(
        "employee.exit.custom.checklist", string="Exit Checklist")

    entry_custom_checklist = fields.Float(
        "Entry Checklist Completed", compute="_compute_entry_custom_checklist", digits=(12, 0))
    exit_custom_checklist = fields.Float(
        "Exit Checklist Completed", compute="_compute_exit_custom_checklist", digits=(12, 0))

    @api.depends("entry_custom_checklist_ids")
    def _compute_entry_custom_checklist(self):
        if self:
            for rec in self:
                total_cnt = self.env[
                    "employee.entry.custom.checklist.line"].search_count([
                        ("employee_id", "=", rec.id),
                    ])
                compl_cnt = self.env[
                    "employee.entry.custom.checklist.line"].search_count([
                        ("employee_id", "=", rec.id),
                        ("state", "=", "completed")
                    ])

                if total_cnt > 0:
                    rec.entry_custom_checklist = (100.0 *
                                                  compl_cnt) / total_cnt
                else:
                    rec.entry_custom_checklist = 0

    entry_custom_checklist_ids = fields.One2many(
        "employee.entry.custom.checklist.line", "employee_id", "Checklist", copy=True)

    @api.depends("exit_custom_checklist_ids")
    def _compute_exit_custom_checklist(self):
        if self:
            for rec in self:
                total_cnt = self.env[
                    "employee.exit.custom.checklist.line"].search_count([
                        ("employee_id", "=", rec.id),
                    ])
                compl_cnt = self.env[
                    "employee.exit.custom.checklist.line"].search_count([
                        ("employee_id", "=", rec.id),
                        ("state", "=", "completed")
                    ])

                if total_cnt > 0:
                    rec.exit_custom_checklist = (100.0 * compl_cnt) / total_cnt
                else:
                    rec.exit_custom_checklist = 0

    exit_custom_checklist_ids = fields.One2many(
        "employee.exit.custom.checklist.line", "employee_id", "Checklist ", copy=True)

    custom_checklist_entry_template_ids = fields.Many2many(
        comodel_name='employee.entry.custom.checklist.template',
        relation='custom_checklist_entry_template_table',
        string='Entry CheckList Template', check_company=True)

    custom_checklist_exit_template_ids = fields.Many2many(
        comodel_name='employee.exit.custom.checklist.template',
        relation='custom_checklist_exit_template_table',
        string='Exit CheckList Template', check_company=True)

    @api.onchange('custom_checklist_entry_template_ids')
    def onchange_custom_checklist_entry_template_ids(self):
        update_ids = []
        for i in self.custom_checklist_entry_template_ids:
            for j in i._origin.entry_checklist_template:
                new_id = self.env[
                    "employee.entry.custom.checklist.line"].create({
                        'name':
                        j.id,
                        'description':
                        j.description
                    })
                update_ids.append(new_id.id)

        self.entry_custom_checklist_ids = [(6, 0, update_ids)]

    @api.onchange('custom_checklist_exit_template_ids')
    def onchange_custom_checklist_exit_template_ids(self):
        update_ids = []
        for i in self.custom_checklist_exit_template_ids:
            for j in i._origin.exit_checklist_template:
                new_id = self.env[
                    "employee.exit.custom.checklist.line"].create({
                        'name':
                        j.id,
                        'description':
                        j.description
                    })
                update_ids.append(new_id.id)

        self.exit_custom_checklist_ids = [(6, 0, update_ids)]
