# -*- coding: utf-8 -*-

from odoo import api, fields, models


class knowsystem_tag(models.Model):
    """
    The model to systemize article tags
    """
    _name = "knowsystem.tag"
    _inherit = ["knowsystem.node"]
    _description = "Tag"

    apply_to_all = fields.Boolean(
        string="Apply to all Documents",
        help="If checked, this tag's articles will be applied to all Odoo objects",
    )
    filter_ids = fields.One2many("knowsystem.filter", "tag_id", string="Applied to Documents")
    parent_id = fields.Many2one("knowsystem.tag", string="Parent Tag")
    child_ids = fields.One2many("knowsystem.tag", "parent_id", string="Child Tags")
    color = fields.Integer(string="Color index", default=10)
    article_ids = fields.Many2many(
        "knowsystem.article",
        "knowsystem_tag_know_system_article_r_table",
        "knowsystem_atricle_r_id",
        "knowsystem_tag_r_id",
        string="Articles",
    )

    _order = "sequence, id"

    @api.model
    def action_return_tags_for_document(self, res_model, res_ids):
        """
        The method to find all available tags for this document

        Args:
         * res_model - model name
         * res_ids - list ids of document

        Methods:
         * _check_document of knowsystem.filter

        Returns:
         * list of ints (knowsystem.tag ids)

        Extra info:
         * use "&" to show tags for all res_id, user "+" to show tags which is suitable for any res_ids
        """
        tags_domain = res_model and [("model", "=", res_model)] or [("id", "<", 0)]
        filters = self.env["knowsystem.filter"].search(tags_domain)
        for res_id in res_ids:
            filters = filters & filters.filtered(lambda filt: filt._check_document(res_id=res_id))
        filter_tags = filters.mapped("tag_id")
        global_tags = self.env["knowsystem.tag"].search([("apply_to_all", "=", True)])
        tags = filter_tags + global_tags
        return tags.ids
