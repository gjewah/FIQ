#coding: utf-8

from odoo import api, fields, models


class knowsystem_article(models.Model):
    """
    Overwrite to add attribute required for documentation
    """
    _name = "knowsystem.article"
    _inherit = "knowsystem.article"

    @api.depends("section_line_ids")
    def _compute_documentation_ids(self):
        """
        Compute method for documentation_ids & used_in_documentation
        """
        for article in self:
            section_ids = article.section_line_ids.mapped("documentation_id")
            section_ids_list = section_ids and section_ids.ids or []
            article.documentation_ids = [(6, 0, section_ids_list)]
            article.used_in_documentation = section_ids_list and True or False

    section_line_ids = fields.One2many("documentation.section.article", "article_id", string="Documentation lines")
    documentation_ids = fields.Many2many(
        "documentation.section",
        "documentation_section_knowsystem_article_id",
        "documentation_section_rel_id",
        "knowsystem_article_id",
        string="Documentation sections",
        compute=_compute_documentation_ids,
        store=True,
        compute_sudo=True,
    )
    used_in_documentation = fields.Boolean(
        "Used for documentation(s)",
        compute=_compute_documentation_ids,
        store=True,
        compute_sudo=True,    
    )
