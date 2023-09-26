# -*- coding: utf-8 -*-

from odoo import fields, models


class custom_article_field(models.Model):
    _inherit = "custom.article.field"
    _portal_object_name = "article_id"
    _portal_views = ["knowsystem_website_custom_fields.knowsystem_article_custom"]

    portal_placement = fields.Selection(
        selection_add=[("left_panel_group", "Left Column"), ("right_panel_group", "Right Column")]
    )
