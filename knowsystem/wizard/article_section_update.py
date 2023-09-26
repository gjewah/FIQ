# -*- coding: utf-8 -*-

from odoo import fields, models


class article_section_update(models.TransientModel):
    """
    The wizard for mass action to update section
    """
    _name = "article.section.update"
    _inherit = "article.mass.update"
    _description = "Update section"

    section_id = fields.Many2one("knowsystem.section", string="New Section", required=True)

    def _update_articles(self, article_ids):
        """
        The method to write category to articles
        
        Args:
         * article_ids - knowsystem.article recordset
        """
        article_ids.write({"section_id": self.section_id.id})
