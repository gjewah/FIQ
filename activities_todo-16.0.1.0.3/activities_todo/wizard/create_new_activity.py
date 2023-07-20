# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class create_new_activity(models.TransientModel):
    """
    The wizard to create a new activity from currently processed
    """
    _name = "create.new.activity"
    _description = "New Activity"

    @api.model
    def _selection_res_reference(self):
        """
        The method to return available for this user models which have message_post methods
        """
        model_ids =  self.env["ir.model"].search([("is_mail_thread", "=", True), ("transient", "=", False)])
        return model_ids.mapped(lambda rec: (rec.model, rec.name))

    @api.depends("res_reference")
    def _compute_res_model_id(self):
        """
        Compute method for res_model_id
        """
        for create_new in self:
            if self.res_reference:
                model_name = self.res_reference._name
                model_id = self.env["ir.model"].search([("model", "=", model_name)], limit=1)
                self.res_model_id = model_id

    @api.onchange("activity_id")
    def _onchange_activity_id(self):
        """
        Onchange method for activity_id
        """
        for create_new in self:
            current_activity = create_new.activity_id
            create_new.activity_type_id = current_activity.activity_type_id
            create_new.summary = current_activity.summary
            create_new.note = current_activity.note
            create_new.user_id = current_activity.user_id
            if current_activity and current_activity.res_id and current_activity.res_model:
                create_new.res_reference = "{},{}".format(current_activity.res_model, current_activity.res_id)
            else:
                create_new.res_reference = False

    @api.onchange("activity_type_id")
    def _onchange_activity_type_id(self):
        """
        Onchange method for activity_type_id

        Methods:
         * _calculate_date_deadline of mail.activity

        Extra info:
         * Expected singleton
        """
        if self.activity_type_id:
            self.summary = self.activity_type_id.summary
            self.date_deadline = self.env["mail.activity"]._calculate_date_deadline(self.activity_type_id)
            self.user_id = self.activity_type_id.default_user_id or self.env.user
            if self.activity_type_id.default_note:
                self.note = self.activity_type_id.default_note

    activity_id = fields.Many2one("mail.activity", string="Activity Reference")
    todo_id = fields.Many2one("mail.activity.todo", string="To Do")
    res_reference = fields.Reference(selection=_selection_res_reference, string="Document", required=True)
    res_model_id = fields.Many2one(
        "ir.model",
        string="Model",
        compute=_compute_res_model_id,
        store=True,
        compute_sudo=True,
    )
    res_model = fields.Char(
        "Related Document Model",
        related="res_model_id.model",
        compute_sudo=True,
        store=True,
        readonly=True,
    )
    activity_type_id = fields.Many2one(
        "mail.activity.type",
        string="Activity",
        domain="['|', ('res_model', '=', False), ('res_model', '=', res_model)]",
        required=True,
    )
    summary = fields.Char("Summary")
    note = fields.Html("Note")
    date_deadline = fields.Date("Due Date", required=True)
    user_id = fields.Many2one("res.users", string="Assigned to", required=True)

    def action_create_new_activity(self):
        """
        The method to create a new activity based on current one

        Extra info:
         * Expected Singleton
        """
        activity_vals = {
            "activity_type_id": self.activity_type_id.id,
            "summary": self.summary,
            "note": self.note,
            "date_deadline": self.date_deadline,
            "user_id": self.user_id.id,
            "res_model_id": self.res_model_id.id,
            "res_id": self.res_reference.id,
        }
        self.env["mail.activity"].create([activity_vals])

    def action_create_new_activity_mark_done(self):
        """
        The method to create a new activity based on current one and mark current done

        Methods:
         * action_create_new_activity
         * action_done of mail.activity.todo

        Extra info:
         * Expected Singleton
        """
        self.action_create_new_activity()
        self.todo_id.action_done()
