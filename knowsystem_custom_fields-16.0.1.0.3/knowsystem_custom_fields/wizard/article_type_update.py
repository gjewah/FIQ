# -*- coding: utf-8 -*-

from odoo import fields, models


class article_type_update(models.TransientModel):
    """
    The wizard for mass action to update type
    """
    _name = "article.type.update"
    _inherit = "article.mass.update"
    _description = "Update type"

    article_type_id = fields.Many2one("article.custom.type", string="New type", required=True)

    def _update_articles(self, article_ids):
        """
        The method to write category to articles
        
        Args:
         * article_ids - knowsystem.article recordset
        """
        article_ids.write({"custom_type_id": self.article_type_id.id})
