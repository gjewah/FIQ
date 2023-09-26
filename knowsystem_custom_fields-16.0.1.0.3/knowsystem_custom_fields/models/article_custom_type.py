#coding: utf-8

from odoo import fields, models


class article_custom_type(models.Model):
    """
    The model to classify articles by types (for custom fields attributes)
    """
    _name = "article.custom.type"
    _inherit = ["article.custom.type", "custom.field.type"]
    _description = "Article Type"
    _custom_field_model = ["custom.article.field"]

    custom_fields_ids = fields.Many2many(
        "custom.article.field",
        "article_custom_type_custom_article_field_reltable",
        "custom_article_field_rel_id",
        "article_custom_type_rel_id",
        string="Custom Fields",
    )

    _order = "sequence,id"
