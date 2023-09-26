#coding: utf-8

from odoo import api, fields, models


class knowsystem_article(models.Model):
    """
    Overwrite too add the translation features
    """
    _inherit = "knowsystem.article"

    @api.depends("create_uid")
    @api.depends_context("lang")
    def _compute_lang(self):
        """
        Compute method for current_lang
        """
        for article in self:
            article.lang = self._context.get("lang")

    def _inverse_name(self):
        """
        Re-write to make inverse with taking into account the context

        Methods:
         * get_installed of res.lang
        """
        lang_ids = self.env["res.lang"].sudo().get_installed()
        for lang in lang_ids:
            super(knowsystem_article, self.with_context(lang=lang[0]))._inverse_name()

    def _inverse_description(self):
        """
        Re-write to make inverse with taking into account the context

        Methods:
         * get_installed of res.lang
        """
        lang_ids = self.env["res.lang"].sudo().get_installed()
        for lang in lang_ids:
            super(knowsystem_article, self.with_context(lang=lang[0]))._inverse_description()

    def _inverse_kanban_manual_description(self):
        """
        Re-write to make inverse with taking into account the context

        Methods:
         * get_installed of res.lang
        """
        lang_ids = self.env["res.lang"].sudo().get_installed()
        for lang in lang_ids:
            super(knowsystem_article, self.with_context(lang=lang[0]))._inverse_kanban_manual_description()

    name = fields.Char(translate=True, inverse=_inverse_name)
    published_name = fields.Char(translate=True, inverse=_inverse_name)
    search_name_key = fields.Char(translate=True)
    description_arch = fields.Html(translate=True)
    description = fields.Html(translate=True, inverse=_inverse_description)
    indexed_description = fields.Text(translate=True)
    kanban_description = fields.Text(translate=True)
    kanban_manual_description = fields.Html(translate=True, inverse=_inverse_kanban_manual_description)
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
                res = super(knowsystem_article, self.with_context(lang=values.get("lang"))).write({
                    "description_arch": values.get("description_arch"),
                    "description": values.get("description"),
                })
                if new_values.get("description"):
                    new_values.pop("description")
                if new_values.get("description_arch"):
                    new_values.pop("description_arch")
            new_values.pop("lang")
        if new_values:
            res = super(knowsystem_article, self).write(new_values)
        return res

    def _prepare_revision_dict(self):
        """
        Rewrite to add lang
        """
        res = super(knowsystem_article, self)._prepare_revision_dict()
        lang = self._context.get("lang") or self.env.user.lang
        res.update({"lang": lang})
        return res
