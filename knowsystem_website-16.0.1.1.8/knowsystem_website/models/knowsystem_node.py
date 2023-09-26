#coding: utf-8

from odoo import fields, models

class knowsystem_node(models.AbstractModel):
    """
    Overwrite to add website settings for tags, sections, and types
    """
    _name = "knowsystem.node"
    _inherit = ["knowsystem.node", "website.multi.mixin", "website.published.mixin"]

    website_published = fields.Boolean(string="Show on Website")
