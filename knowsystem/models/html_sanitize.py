# -*- coding: utf-8 -*-

from lxml import html

from odoo import models
from odoo.fields import Html

LAYOUT_SELECTOR = "//table[hasclass('knowsystem_layout')]"


class KnowSystemHtml(Html):
    """
    Introduce own HTML field to avoid sanitizing articles' content
    """
    def _convert(self, value, record, validate):
        """
        Overwrite to save previous knowsystem_layout elements and restore them after sanitizing
        In this way, knowsystem elements will not be sanitized
        """
        if value and value.find("knowsystem_layout") != -1:
            html_value = html.fromstring(value)
            kms_articles = html_value.xpath(LAYOUT_SELECTOR)
            result = super()._convert(value, record, validate)
            sanitized_html_value = html.fromstring(result)
            sanitized_articles = sanitized_html_value.xpath(LAYOUT_SELECTOR)
            for sanitized_article in sanitized_articles:
                sanitized_article.getparent().replace(sanitized_article, kms_articles[0])
                kms_articles.pop(0)
            return html.tostring(sanitized_html_value).decode("utf-8")
        return super()._convert(value, record, validate)


class mail_compose_message(models.TransientModel):
    """
    Ovewrite to change the field type for its own
    """
    _inherit = "mail.compose.message"

    body = KnowSystemHtml()


class mail_message(models.Model):
    """
    Ovewrite to change the field type for its own
    """
    _inherit = "mail.message"

    body = KnowSystemHtml()


class mail_activity(models.Model):
    """
    Ovewrite to change the field type for its own
    """
    _inherit = "mail.activity"

    note = KnowSystemHtml()
