# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class MeetingCustomChecklist(models.Model):
    _name = "meeting.custom.checklist"
    _description = "Meeting Custom Checklist"
    _order = 'name, id'

    name = fields.Char("Checklist", required=True)


class MeetingCustomChecklistLine(models.Model):
    _name = "meeting.custom.checklist.line"
    _description = "Meeting Custom Checklist Line"
    _order = "id desc"

    name = fields.Many2one("meeting.custom.checklist", required=True)
    state = fields.Selection([("new", "New"), ("completed", "Completed"),
                              ("cancelled", "Cancelled")],
                             default="new",
                             readonly=True,
                             index=True)

    calendar_id = fields.Many2one("calendar.event")

    def btn_check(self):
        for rec in self:
            rec.write({"state": "completed"})

    def btn_close(self):
        for rec in self:
            rec.write({"state": "cancelled"})
