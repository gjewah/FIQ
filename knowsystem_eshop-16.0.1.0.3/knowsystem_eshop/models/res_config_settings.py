# -*- coding: utf-8 -*-

from odoo import fields, models


class res_config_settings(models.TransientModel):
    """
    Overwrite to add eshop-specific settings
    """
    _inherit = "res.config.settings"

    def _default_faq_website_id(self):
        """
        Default method for faq_website_id
        """
        return self.env["website"].search([("company_id", "=", self.env.company.id)], limit=1)

    faq_website_id = fields.Many2one(
        "website",
        string="FAQ Website",
        default=_default_faq_website_id,
        ondelete="cascade",
    )
    knowsystem_eshop_type = fields.Selection(related="faq_website_id.knowsystem_eshop_type", readonly=False)
    knowsystem_faq_style = fields.Char(related="faq_website_id.knowsystem_faq_style", readonly=False)
    knowsystem_faq_section_ids = fields.Many2many(related="faq_website_id.knowsystem_faq_section_ids", readonly=False)
    knowsystem_faq_tag_ids = fields.Many2many(related="faq_website_id.knowsystem_faq_tag_ids", readonly=False)
    knowsystem_faq_article_ids = fields.Many2many(related="faq_website_id.knowsystem_faq_article_ids", readonly=False)
