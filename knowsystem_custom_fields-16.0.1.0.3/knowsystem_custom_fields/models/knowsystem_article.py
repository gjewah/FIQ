#coding: utf-8

from odoo import api, fields, models


class knowsystem_article(models.Model):
    """
    Overwrite to add type
    """
    _inherit = "knowsystem.article"

    custom_type_id = fields.Many2one("article.custom.type", string="Article Type", index=True)

    @api.model
    def action_return_types(self):
        """
        The method to return article types

        Methods:
         * return_nodes of knowsytem.node
        """
        return self.env["article.custom.type"]._return_nodes()
