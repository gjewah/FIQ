# -*- coding: utf-8 -*-

from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteSale(WebsiteSale):
    """
    Overwrite to add FAQ features
    """
    @http.route(["/shop/knowsystem_faq"], type="json", auth="public", methods=["POST"], website=True, csrf=False)
    def show_knowsystem_faq(self, template_id, attr_values):
        """
        The method to find product FAQ and show them based on the specified method

        Args:
         * template_id - int - id of considered product.template
         * attr_values - list - ids of chosen attribute values. MIGHT BE EMPTY!

        Methods:
         * action_return_faq of product.template

        Returns:
         * dict (@see action_return_faq of product.template)
        """
        product_id = request.env["product.template"].browse(template_id).exists()
        article_ids = False
        if product_id:
            article_ids = product_id.action_return_faq(attr_values, request.website)
        return article_ids
