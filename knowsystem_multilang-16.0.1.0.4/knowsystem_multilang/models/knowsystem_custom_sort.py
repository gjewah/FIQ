# -*- coding: utf-8 -*-

from odoo import fields, models


class knowsystem_custom_sort(models.Model):
    """
    Overwrite too add the translation features
    """
    _inherit = "knowsystem.custom.sort"

    name = fields.Char(translate=True)
