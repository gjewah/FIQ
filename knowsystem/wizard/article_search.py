# -*- coding: utf-8 -*-

from odoo import api, fields, models


class article_search(models.TransientModel):
    """
    The wizard to apply quick articles search and referencing those if needed
    """
    _name = "article.search"
    _description = "Search Articles"

    @api.model
    def _default_tag_ids(self):
        """
        Default method for tag_ids

        Methods:
         * action_return_tags_for_document of knowsystem.tag

        Returns:
         * list of ints
        """
        tag_ids = []
        kms_model = self._context.get("kms_model")
        if kms_model:
            kms_res_ids = self._context.get("kms_res_ids") or []
            tag_ids = self.env["knowsystem.tag"].action_return_tags_for_document(kms_model, kms_res_ids)
        return tag_ids

    @api.depends("section_ids", "tag_ids", "search", "selected_article_ids")
    def _compute_article_ids(self):
        """
        Compute method for article_ids
        """
        for wizard in self:
            domain = wizard._get_domain()
            article_ids = self.env["knowsystem.article"]._search(domain)
            self.article_ids = [(6, 0, article_ids)]

    section_ids = fields.Many2many("knowsystem.section", string="Sections")
    tag_ids = fields.Many2many("knowsystem.tag", string="Tags", default=_default_tag_ids)
    search = fields.Char(string="Search in contents")
    article_ids = fields.Many2many("knowsystem.article", string="Articles", compute=_compute_article_ids)
    selected_article_ids = fields.Many2many(
        "knowsystem.article",
        "knowsystem_article_article_search_selected_rel_table",
        "knowsystem_selected_article_id",
        "article__selected_search_id",
        string="Selected Articles",
    )
    no_selection = fields.Boolean(string="No selection", default=False)

    def _get_domain(self):
        """
        The method to get wizard domain based on introduced field values

        Returns:
         * list - RPR
        """
        domain = []
        if self.selected_article_ids:
            domain += [("id", "not in", self.selected_article_ids.ids)]
        if self.section_ids:
            domain += [("section_id", "child_of", self.section_ids.ids)]
        if self.tag_ids:
            domain += [("tag_ids", "child_of", self.tag_ids.ids)]
        if self.search:
            domain += ["|", ("name", "ilike", self.search), ("indexed_description", "ilike", self.search)]
        return domain
