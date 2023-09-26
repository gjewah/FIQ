# -*- coding: utf-8 -*-

from odoo import api, fields, models


class article_copy_language(models.TransientModel):
    """
    The model is the wizard to replace the current content with the translated content
    """
    _name = "article.copy.language"
    _description = "Copy Translation"

    @api.model
    def _lang_get(self):
        """
        The method to prepare the selection of the available languages
        """
        return self._get_langs()

    @api.model
    def _default_lang(self):
        """
        Default method for lang
        """
        all_langs = self._get_langs()
        return all_langs and all_langs[0][0] or False

    @api.depends("lang", "article_id")
    def _compute_description_arch(self):
        """
        Compute method for description_arch
        """
        for wiz in self:
            wiz.description_arch = wiz.article_id.with_context(lang=wiz.lang).description_arch

    lang = fields.Selection(_lang_get,  string="From Language", required=True, default=_default_lang)
    article_id = fields.Many2one("knowsystem.article", string="Article", required=True)
    description_arch = fields.Text(string="Translation", compute=_compute_description_arch)

    @api.model
    def _get_langs(self):
        """
        The method to get available languages

        Returns:
         * list of tuples
        """
        langs_list = self.env["res.lang"].get_installed()
        langs = [lang for lang in langs_list if lang[0] != self._context.get("target_lang")]
        return langs
