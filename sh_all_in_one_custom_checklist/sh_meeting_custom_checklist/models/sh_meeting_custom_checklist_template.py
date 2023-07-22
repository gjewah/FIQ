# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class MeetingCustomChecklistTemplate(models.Model):
    _name = "meeting.custom.checklist.template"
    _description = "Meeting Custom Checklist Template"
    _order = 'name, id'

    name = fields.Char(required=True)
    checklist_template_ids = fields.Many2many('meeting.custom.checklist',
                                          string="Check List")
