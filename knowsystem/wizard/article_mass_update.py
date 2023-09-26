# -*- coding: utf-8 -*-

from odoo import api, fields, models


class article_mass_update(models.TransientModel):
    """
    The wizard to be inherited in any update wizard that assumes writing mass values in articles
    """
    _name = "article.mass.update"
    _description = "Articles Update"

    @api.model
    def _default_article_ids(self):
        """
        Default method for article_ids. Primarily needed when there are no default_article_ids (that actually
        is passed without any further interaction)
        """
        return self._context.get("default_article_ids") or self._context.get("active_ids") or []

    article_ids = fields.Many2many("knowsystem.article", string="Articles", default=_default_article_ids)

    @api.model_create_multi
    def create(self, vals_list):
        """
        Overwrite to trigger articles update
        The idea is to use standard 'Save' buttons and do not introduce its own footer for each mass action wizard

        Methods:
         * action_update_products
        """
        wizards = super(article_mass_update, self).create(vals_list)
        wizards.action_update_articles()
        return wizards

    def action_update_articles(self):
        """
        The method to update articles in batch

        Methods:
         * _update_articles
        """
        for wizard in self:
            if wizard.article_ids:
                wizard._update_articles(wizard.article_ids)

    def _update_articles(self, article_ids):
        """
        Dummy method to prepare values
        It is to be inherited in a real update wizard

        Args:
         * article_ids - knowsystem.article recordset
        """
        pass
