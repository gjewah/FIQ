# -*- coding: utf-8 -*-

from odoo import fields, models


class article_update(models.TransientModel):
    """
    Introduce for knowsystem migration
    """
    _name = "article.update"
    _description = "Update article (obsolete)"

    activate = fields.Selection([("activate", "Restore"), ("archive", "Archive")], string="Update state")
