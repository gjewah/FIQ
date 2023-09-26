# -*- coding: utf-8 -*-

from odoo import fields, models


class knowsystem_custom_search(models.Model):
    """
    Overwrite too add the translation features
    """
    _inherit = "knowsystem.custom.search"

    name = fields.Char(translate=True)
