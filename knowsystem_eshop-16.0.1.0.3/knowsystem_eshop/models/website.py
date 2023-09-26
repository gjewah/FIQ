#coding: utf-8

from odoo import _, fields, models

DEFAULT_BUTTON = _("<i class='fa fa-info-circle'> </i> Frequently asked questions")


class website(models.Model):
    """
    Overwrite to keep FAQ configuration for particular website
    """
    _inherit = "website"

    knowsystem_eshop_type = fields.Selection(
        [
            ("link", "KnowSystem portal link"),
            ("popup", "Popup accordion"),
            ("no", "Do not show"),
        ],
        string="FAQ view",
        default="link",
    )
    knowsystem_faq_style = fields.Char(string="FAQ button text", default=DEFAULT_BUTTON, translate=True)
    knowsystem_faq_section_ids = fields.Many2many(
        "knowsystem.section",
        "knowsystem_section_website_faq_rel_table",
        "knowsystem_section_rel_id",
        "website_rel_id",
        string="KnowSystem sections",
    )
    knowsystem_faq_tag_ids = fields.Many2many(
        "knowsystem.tag",
        "knowsystem_tag_website_faq_rel_table",
        "knowsystem_tag_rel_id",
        "website_rel_id",
        string="KnowSystem tags",
    )
    knowsystem_faq_article_ids = fields.Many2many(
        "knowsystem.article",
        "knowsystem_article_website_faq_rel_table",
        "knowsystem_article_rel_id",
        "website_rel_id",
        string="KnowSystem articles",
    )
