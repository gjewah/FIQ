# -*- coding: utf-8 -*-

from odoo import fields, models


class knowsystem_node(models.AbstractModel):
    """
    Overwrite too add the translation features
    """
    _inherit = "knowsystem.node"

    name = fields.Char(translate=True)
    description = fields.Html(translate=True)
