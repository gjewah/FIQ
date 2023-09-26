# -*- coding: utf-8 -*-

from odoo import api, fields, models


class add_to_documentation(models.TransientModel):
    """
    The wizard for mass action to add articles to the documentation
    """
    _name = "add.to.documentation"
    _inherit = "article.mass.update"
    _description = "Add articles to the documentation"

    @api.model
    def _security_action_selection(self):
        """
        Method to get available security actions options
        """
        return self.env["documentation.section.article"]._security_action_selection()

    section_id = fields.Many2one("documentation.section", string="Section", required=True)
    security_action = fields.Selection(_security_action_selection, string="Security Action", default=False)
    version_ids = fields.Many2many(
        "documentation.version",
        "documentation_version_add_to_documentation_article_rel_table",
        "documentation_version_rel_id",
        "add_to_documentation_rel_id",
        string="Versions",
    )

    def _update_articles(self, article_ids):
        """
        The method to process articles and them to the documentation correctly

        Args:
         * article_ids - knowsystem.article recordset
        """
        vals_list = []
        max_sequence = self.section_id.article_ids and self.section_id.article_ids[-1].sequence + 1 or 0
        for article in article_ids:
            values = {
                "documentation_id": self.section_id.id,
                "article_id": article.id,
                "sequence": max_sequence,
                "security_action": self.security_action,
                "version_ids": [(6, 0, self.version_ids.ids or [])],
            }
            vals_list.append(values)
            max_sequence += 1
        self.env["documentation.section.article"].create(vals_list)
