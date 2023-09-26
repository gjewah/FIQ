# -*- coding: utf-8 -*-

from odoo import fields, models


class article_groups_update(models.TransientModel):
    """
    The wizard for mass action to update groups
    """
    _name = "article.groups.update"
    _inherit = "article.mass.update"
    _description = "Update groups"

    add_user_group_ids = fields.Many2many(
        "res.groups",
        "res_groups_article_groups_update_add_read_rel_table",
        "res_groups_id",
        "article_groups_update_id",
        string="Add read access groups",
    )
    remove_user_group_ids = fields.Many2many(
        "res.groups",
        "res_groups_article_groups_update_remove_read_rel_table",
        "res_groups_id",
        "article_groups_update_id",
        string="Remove read access groups",
    )
    add_edit_user_group_ids = fields.Many2many(
        "res.groups",
        "res_groups_article_groups_update_add_edit_rel_table",
        "res_groups_id",
        "article_groups_update_id",
        string="Add edit access groups",
    )
    remove_edit_user_group_ids = fields.Many2many(
        "res.groups",
        "res_groups_article_groups_update_remove_edit_rel_table",
        "res_groups_id",
        "article_groups_update_id",
        string="Remove edit access groups",
    )

    def _update_articles(self, article_ids):
        """
        The method to write new access groups to articles
        
        Args:
         * article_ids - knowsystem.article recordset
        """
        update_values = {}
        updated_read_groups = []
        update_edit_groups = []
        if self.add_user_group_ids:
            for group in self.add_user_group_ids:
                updated_read_groups.append((4, group.id))
        if self.remove_user_group_ids:
            for group in self.remove_user_group_ids:
                updated_read_groups.append((3, group.id))
        if self.add_edit_user_group_ids:
            for group in self.add_edit_user_group_ids:
                update_edit_groups.append((4, group.id))
        if self.remove_edit_user_group_ids:
            for group in self.remove_edit_user_group_ids:
                update_edit_groups.append((3, group.id))
        if updated_read_groups:
            update_values.update({"user_group_ids": updated_read_groups})
        if update_edit_groups:
            update_values.update({"edit_user_group_ids": update_edit_groups})
        if update_values:
            article_ids.write(update_values)
