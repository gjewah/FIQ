# -*- coding: utf-8 -*-

from odoo import fields, models


class color_code_partner(models.Model):
    """
    Introducing the model to link color code and a partner
    """
    _name = "color.code.partner"
    _description = "Color Code Note"

    color_code_id = fields.Many2one("color.code", string="Color Code", ondelete="cascade", index=True)
    partner_id = fields.Many2one("res.partner", string="Contact", ondelete="cascade")
    name = fields.Text(string="Description")
    user_id = fields.Many2one("res.users", string="Author", default=lambda self: self.env.user)
    comment_datetime = fields.Datetime(string="Date", default=lambda self: fields.Datetime.now())

    _order = "color_code_id, id"
