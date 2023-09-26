# -*- coding: utf-8 -*-

from odoo import fields, models


class article_custom_type(models.Model):
    """
    Introduced here to avoid inheritance issues
    """
    _name = "article.custom.type"
    _inherit = ["knowsystem.node"]
    _description = "Article Type"

    parent_id = fields.Many2one("article.custom.type", string="Parent Type")
    child_ids = fields.One2many("article.custom.type", "parent_id", string="Child Types")
