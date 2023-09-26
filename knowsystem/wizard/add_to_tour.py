# -*- coding: utf-8 -*-

from odoo import fields, models


class add_to_tour(models.TransientModel):
    """
    The wizard for mass action to add articles to the tour
    """
    _name = "add.to.tour"
    _inherit = "article.mass.update"
    _description = "Add articles to the tour"

    tour_id = fields.Many2one("knowsystem.tour", string="Tour", required=True)

    def _update_articles(self, article_ids):
        """
        The method to process articles and them to the tour correctly

        Args:
         * article_ids - knowsystem.article recordset
        """
        vals_list = []
        max_sequence = self.tour_id.tour_article_ids and self.tour_id.tour_article_ids[-1].sequence + 1 or 0
        for article in article_ids:
            values = {"tour_id": self.tour_id.id, "article_id": article.id, "sequence": max_sequence}
            vals_list.append(values)
            max_sequence += 1
        self.env["knowsystem.tour.article"].create(vals_list)
