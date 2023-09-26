# -*- coding: utf-8 -*-

from odoo import fields, models


class custom_article_field(models.Model):
    _name = "custom.article.field"
    _inherit = ["custom.extra.field"]
    _description = "Custom Article Field"
    _field_code = "artl"
    _linked_model = "knowsystem.article"
    _type_field = "custom_type_id"
    _type_field_model = "article.custom.type"
    _backend_views = ["knowsystem_custom_fields.knowsystem_article_view_form_custom"]

    types_ids = fields.Many2many(
        "article.custom.type",
        "article_custom_type_custom_article_field_reltable",
        "article_custom_type_rel_id",
        "custom_article_field_rel_id",
        string="Types",
        help="Leave it empty, if this field should appear for all articles disregarding type"
    )
    placement = fields.Selection(
        selection_add=[
            ("left_panel_group", "Left Column"),
            ("right_panel_group", "Right Column"),
            ("after_description_group", "After Article"),
        ],
        default="after_description_group",
    )
    sel_options_ids = fields.One2many(context={"default_model": "custom.article.field"})
