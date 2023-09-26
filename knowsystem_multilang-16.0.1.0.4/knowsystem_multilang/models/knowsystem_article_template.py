# -*- coding: utf-8 -*-

from odoo import api, fields, models


class knowsystem_article_template(models.Model):
    """
    Overwrite too add the translation features
    """
    _inherit = "knowsystem.article.template"

    @api.depends("create_uid")
    @api.depends_context("lang")
    def _compute_lang(self):
        """
        Compute method for current_lang
        """
        for template in self:
            template.lang = self._context.get("lang")

    name = fields.Char(translate=True)
    description_arch = fields.Html(translate=True)
    description = fields.Html(translate=True)
    lang = fields.Char(string="Current Language", compute=_compute_lang, store=False)

    def write(self, values):
        """
        Re-write to save description and description_arch in the selected language
        If 'lang' is specifiedm then it was selected at least once and we cannot rely upon context language
        Then, we write separately descriptions with the proper context (affected by language) and other values
        This affects revisions, since revisions might have different languages and should be saved separately
        """
        new_values = values.copy()
        if values.get("lang") and values.get("lang") != self._context.get("lang"):
            if (values.get("description") is not None or values.get("description_arch") is not None):
                res = super(knowsystem_article_template, self.with_context(lang=values.get("lang"))).write({
                    "description_arch": values.get("description_arch"),
                    "description": values.get("description"),
                })
                if new_values.get("description"):
                    new_values.pop("description")
                if new_values.get("description_arch"):
                    new_values.pop("description_arch")
            new_values.pop("lang")
        if new_values:
            res = super(knowsystem_article_template, self).write(new_values)
        return res
