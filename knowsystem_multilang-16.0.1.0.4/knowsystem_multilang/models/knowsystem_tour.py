#coding: utf-8

from odoo import fields, models

class knowsystem_tour(models.Model):
    """
    Overwrite too add the translation features
    """
    _inherit = "knowsystem.tour"

    name = fields.Char(translate=True)
    description = fields.Html(translate=True)
