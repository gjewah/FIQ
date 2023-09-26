#coding: utf-8

from odoo import fields, models


class knowsystem_by_attribute(models.Model):
    """
    The model to structure KPIs and targets
    """
    _name = "knowsystem.by.attribute"
    _description = "Attribute FAQ"

    template_id = fields.Many2one("product.template", string="Applied for template", ondelete="cascade")
    attribute_id = fields.Many2one("product.attribute", string="Applied for attribute", ondelete="cascade")
    section_ids = fields.Many2many(
        "knowsystem.section",
        "knowsystem_section_knowsystem_by_attribute_rel_table",
        "knowsystem_section_rel_id",
        "knowsystem_by_attribute_rel_id",
        string="KnowSystem Sections",
    )
    tag_ids = fields.Many2many(
        "knowsystem.tag",
        "knowsystem_tag_knowsystem_by_attribute_rel_table",
        "knowsystem_tag_rel_id",
        "knowsystem_by_attribute_rel_id",
        string="KnowSystem Tags",
    )
    article_ids = fields.Many2many(
        "knowsystem.article",
        "knowsystem_article_knowsystem_by_attribute_rel_table",
        "knowsystem_article_rel_id",
        "knowsystem_by_attribute_rel_id",
        string="KnowSystem Articles",
    )
    value_ids = fields.Many2many(
        "product.attribute.value",
        "product_attribute_value_knowsystem_by_attribute_rel_table",
        "product_attribute_value_id",
        "knowsystem_by_attribute_rel_id",
        string="Applied only for values",
    )
