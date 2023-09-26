#coding: utf-8

from odoo import fields, models


class product_attribute(models.Model):
    """
    Overwrite to establish direct link between attributes and articles
    """
    _inherit = "product.attribute"

    knowsystem_by_attribute_ids = fields.One2many("knowsystem.by.attribute", "attribute_id", string="KnowSystem FAQ")
