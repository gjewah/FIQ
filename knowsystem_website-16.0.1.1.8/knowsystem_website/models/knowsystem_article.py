#coding: utf-8

from odoo import _, api, fields, models
from odoo.addons.http_routing.models.ir_http import slug


class knowsystem_article(models.Model):
    """
    Overwrite to add portal and website attributes
    """
    _name = "knowsystem.article"
    _inherit = [
        "knowsystem.article", "website.published.mixin", "website.multi.mixin", "website.seo.metadata", "portal.mixin"
    ]

    @api.model
    def _selection_editor_types(self):
        """
        Overwrite to add website builder as the option
        """
        res = super(knowsystem_article, self)._selection_editor_types()
        res.insert(0, ("website_editor", _("Website Builder")))
        return res

    @api.depends("tag_ids","tag_ids.all_partner_ids")
    def _compute_access_partner_ids(self):
        """
        Compute method for all_partner_ids
        """
        self.clear_caches() # to avoid taking parent-related cache and sudden error
        for article in self:
            article.access_partner_ids = article.tag_ids.mapped("all_partner_ids")

    def _compute_full_website_url(self):
        """
        Overwritting the compute method for portal_url to pass our pathes

        Methods:
         * super
        """
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for article in self:
            website_url = article.website_id and article.website_id.domain or base_url
            article.full_website_url = "{}{}".format(website_url, article.website_url)

    def _compute_website_url(self):
        """
        Overwritting the compute method for portal_url to pass our pathes

        Methods:
         * super
        """
        super(knowsystem_article, self)._compute_website_url()
        for article in self:
            article.website_url = u"/knowsystem/{}".format(slug(article))

    def _compute_access_url(self):
        """
        Overwritting the compute method for access_url to pass our pathes

        Methods:
         * super
        """
        for article in self:
            article.access_url = article.website_url

    editor_type = fields.Selection(_selection_editor_types)
    access_partner_ids = fields.Many2many(
        "res.partner",
        "res_partner_knowsystem_article_security_rel_table",
        "res_partner_id",
        "knowsystem_article_id",
        string="Access Partners",
        compute=_compute_access_partner_ids,
        compute_sudo=True,
        store=True,
        recursive=True,
    )
    full_website_url = fields.Char("Full Website URL", compute=_compute_full_website_url)
    website_pinned = fields.Boolean(
        string="Website Pinned",
        default=False,
        help="If checked, such an article will be shown always above all articles disregarding active page, which\
sections, or tags are selected",
    )
