#coding: utf-8

from odoo import api, fields, models


class knowsystem_article_revision(models.Model):
    """
    Overwrite too add the translation features
    """
    _inherit = "knowsystem.article.revision"

    @api.model
    def _lang_get(self):
        """
        The method to prepare the selection of the available languages
        """
        return self.env["res.lang"].get_installed()

    lang = fields.Selection(_lang_get, string="Language", default=lambda self: self.env.user.lang)

    def _prepare_revision_dict(self):
        """
        Override to exclude not current user language revision
        """
        res = {}
        if self.env.user.lang == self.lang:
            res = super(knowsystem_article_revision, self)._prepare_revision_dict()
        return res

    def _return_previous_revision_domain(self):
        """
        Overrride to add lang to domain
        """
        res = super(knowsystem_article_revision, self)._return_previous_revision_domain()
        res.append(("lang", "=", self.lang))
        return res

    def action_recover_this_revision(self):
        """
        Override to pass language
        """
        return super(knowsystem_article_revision, self.with_context(lang=self.lang)).action_recover_this_revision()
