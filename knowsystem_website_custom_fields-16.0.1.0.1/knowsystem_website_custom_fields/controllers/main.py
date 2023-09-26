# -*- coding: utf-8 -*-

from odoo.http import request
from odoo.addons.knowsystem_website.controllers.main import CustomerPortal


class CustomerPortal(CustomerPortal):
    """
    Overwritting to load types
    """
    def _prepare_articles_helper(self, page=1, sections=None, tags=None, types=None, sortby=None, filterby=None,
        search=None, search_in="content", domain=[], url="/knowsystem", **kw):
        """
        Re-write to load types

        Methods:
         * _return_navigation_elements
        """
        values = super(CustomerPortal, self)._prepare_articles_helper(
            page=page, sections=sections, tags=tags, types=types, sortby=sortby, filterby=filterby, search=search,
            search_in=search_in, domain=domain, url=url, **kw
        )
        website_id = request.website
        show_tooltip = website_id.knowsystem_portal_tooltip
        type_ids = self._return_navigation_elements("article.custom.type", website_id, show_tooltip)
        values.update({"type_ids": type_ids})
        return values
