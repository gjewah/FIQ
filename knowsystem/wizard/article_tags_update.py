# -*- coding: utf-8 -*-

from odoo import fields, models


class article_tags_update(models.TransientModel):
    """
    The wizard for mass action to update tags
    """
    _name = "article.tags.update"
    _inherit = "article.mass.update"
    _description = "Update tags"

    to_add_tag_ids = fields.Many2many(
        "knowsystem.tag",
        "knowsystem_tag_article_update_add_rel_table",
        "knowsystem_tag_add_id",
        "article_add_tag_id",
        string="Add tags",
    )
    to_remove_tag_ids = fields.Many2many(
        "knowsystem.tag",
        "knowsystem_tag_article_update_remove_rel_table",
        "knowsystem_tag_remove_id",
        "article_add_remove_id",
        string="Remove tags",
    )

    def _update_articles(self, article_ids):
        """
        The method to write new tags to articles
        
        Args:
         * article_ids - knowsystem.article recordset
        """
        updated_tags = []
        if self.to_add_tag_ids:
            for tag in self.to_add_tag_ids:
                updated_tags.append((4, tag.id))
        if self.to_remove_tag_ids:
            for tag in self.to_remove_tag_ids:
                updated_tags.append((3, tag.id))
        if updated_tags:
            article_ids.write({"tag_ids": updated_tags})
