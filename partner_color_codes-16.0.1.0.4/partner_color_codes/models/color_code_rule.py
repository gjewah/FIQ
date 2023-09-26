# -*- coding: utf-8 -*-

from odoo import fields, models


class color_code_rule(models.Model):
    """
    Introducing the model to search a partner and assign a color code
    """
    _name = "color.code.rule"
    _description = "Color Code Rule"

    name = fields.Text(string="Rule Description")
    color_code_id = fields.Many2one("color.code", string="Color Code", required=True, ondelete="cascade", index=True)
    domain = fields.Text(string="Filters", default="[]")

    _order = "color_code_id, id"
