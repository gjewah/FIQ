# -*- coding: utf-8 -*-

from werkzeug.urls import url_encode

from odoo import _, http, SUPERUSER_ID
from odoo.addons.knowsystem_website.controllers.main import CustomerPortal, pre_process_print_name
from odoo.http import request
from odoo.tools import consteq


class CustomerPortal(CustomerPortal):
    """
    The controller to manage pages related to documentation
    """
    def _prepare_home_portal_values(self, counters):
        """
        Overwrite to understand wheter the portal entry should be shown
        """
        values = super(CustomerPortal, self)._prepare_home_portal_values(counters)
        if "documentation_count" in counters:
            values.update({"documentation_count": request.website.documentation_builder_portal and _("docs") or 0})
        return values

    def _check_docs_kms_options(self):
        """
        The method to take into account whether KnowSystem is turn on of portal (needed for internal and portal users)
        and for website (needed for public users)

        Returns:
         * False if rights are correct
         * 403 redirection if failed
        """
        website_id = request.website
        internal = request.env.user.has_group("base.group_user") or request.env.user.has_group("base.group_portal")
        res = False
        if (not internal and not website_id.documentation_builder_portal) \
                or (internal and not website_id.documentation_builder_public):
            res = request.render("http_routing.403")
        return res

    def _print_section_articles(self, article_ids):
        """
        The method to make the printing request

        Args:
         * article_ids - knowsystem.article recordset

        Returns:
         * Response
        """
        if article_ids:
            lang = request.env.context.get("lang") or request.env.user.lang
            pdf_content, mimetype = request.env["ir.actions.report"]._render_qweb_pdf(
                "knowsystem.action_report_knowsystem_article", article_ids.ids, {}
            )
            pdfhttpheaders = [("Content-Type", "application/pdf"), ("Content-Length", len(pdf_content))]
            res = request.make_response(pdf_content, headers=pdfhttpheaders)
        else:
            res = request.render("http_routing.404")
        return res

    @http.route(["/docs"], type="http", auth="public", website=True, sitemap=True)
    def documentation_sections_overview(self, **kw):
        """
        The route to open documentation sections page
        """
        res = self._check_docs_kms_options()
        if not res:
            search_context = request.env.context.copy()
            if kw.get("search"):
                search_context.update({"docu_section_search": kw.get("search")})
            categories = request.env["documentation.category"].search([
                ("website_published", "=", True), 
                ("website_id", "in", (False, request.website.id)),
            ])
            # to avoid showing empty for this user catgeories
            categories = categories.filtered(
                lambda categ: categ.with_context(search_context).get_sections_with_context()
            )
            values = {
                "categories": categories.with_context(search_context),
                "docu_section_search": kw.get("search") and kw.get("search") or "",
            }
            res = request.render("documentation_builder.documentation_overview", values)
        return res

    @http.route(["/docs/<model('documentation.section'):doc_section_id>",], type="http", auth="public", website=True, 
        sitemap=True)
    def documentation_section(self, doc_section_id=None, **kw):
        """
        The route to open specified documentation section (with default version)

        Methods:
         * _prepare_content_and_toc of documentatation.section
         * pre_process_print_name
        """
        res = self._check_docs_kms_options()
        if not res:
            versioning_option = request.env.user.has_group("documentation_builder.group_documentation_versioning")
            current_version = current_version_name = False
            available_versions = []
            if versioning_option:
                current_version = kw.get("version_id")
                if current_version:
                    try:
                        current_version_obj = request.env["documentation.version"].browse(current_version)
                        current_version_name = current_version_obj.name_get()[0][1]
                    except:
                        # if not correct version id 
                        current_version = False
                # in case we are under section sudo
                available_version_ids = request.env["documentation.version"].search([
                    ("id", "in", doc_section_id.version_ids.ids),
                    ("active", "=", True),
                ]) 
                available_versions = available_version_ids.name_get()
                if available_versions and (not current_version or current_version not in available_version_ids.ids):
                    current_version = available_versions[0][0]
                    return request.redirect("/docs/{}/{}?{}".format(current_version, doc_section_id.id, url_encode(kw)))
            articles, toc = doc_section_id._prepare_content_and_toc(request.website, versioning_option, current_version)
            values = {
                "main_object": doc_section_id,
                "articles": articles,
                "toc": toc,
                "page_name": "{}".format(doc_section_id.name),
                "available_versions": available_versions,
                "current_version": current_version,
                "current_version_name": current_version_name,
                "versioning_option": versioning_option,
                "url_main": "docs",
                "section_safe_name": pre_process_print_name(doc_section_id.name),
            }
            res = request.render("documentation_builder.documentation", values)        
        return res

    @http.route(["/docs/<int:doc_version_id>/<model('documentation.section'):doc_section_id>"], type="http", 
        auth="public", website=True, sitemap=True)
    def documentation_section_version(self, doc_version_id=None, doc_section_id=None, **kw):
        """
        The route to open specified documentation section
        """
        versioning_option = request.env.user.has_group("documentation_builder.group_documentation_versioning")
        res = False
        if not versioning_option or not doc_version_id:
            # if versioning is not turned on or its is zero (global)
            res = request.redirect("/docs/{}?{}".format(doc_section_id.id, url_encode(kw)))
        else:
            kw.update({"version_id": doc_version_id})
            res = self.documentation_section(doc_section_id=doc_section_id, **kw)
        return res

    @http.route(["/doctoken/<int:docint>"], type="http", auth="public", website=True, sitemap=False)
    def documentation_section_token(self, docint=None, **kw):
        """
        The route to open the article page by access token

        Methods:
         * _check_docs_kms_options
         * update_number_of_views of knowsystem.article
         * _prepare_portal_layout_values
        """
        doc_section_id = request.env["documentation.section"].sudo().browse(docint)
        if not doc_section_id or not doc_section_id.exists() or not kw.get("access_token") \
                or not consteq(doc_section_id.access_token, kw.get("access_token")):
            res = request.render("http_routing.404")
        else:
            # SUPERUSER_ID is required for check rights because of has_group
            doc_section_id = doc_section_id.sudo().with_user(SUPERUSER_ID)
            versioning_option = request.env.user.has_group("documentation_builder.group_documentation_versioning")
            current_version = current_version_name = False
            available_versions = []
            if versioning_option:
                current_version = kw.get("version_id")
                if current_version:
                    try:
                        current_version_obj = request.env["documentation.version"].browse(current_version)
                        current_version_name = current_version_obj.name_get()[0][1]
                    except:
                        # if not correct version id 
                        current_version = False
                # in case we are under section sudo
                available_version_ids = request.env["documentation.version"].search([
                    ("id", "in", doc_section_id.version_ids.ids),
                    ("active", "=", True),
                ]) 
                available_versions = available_version_ids.name_get()
                if available_versions and (not current_version or current_version not in available_version_ids.ids):
                    current_version = available_versions[0][0]
                    return request.redirect(
                        "/docstokenmulti/{}/{}?{}".format(current_version, doc_section_id.id, url_encode(kw))
                    )
            articles, toc = doc_section_id._prepare_content_and_toc(request.website, versioning_option, current_version)
            values = {
                "main_object": doc_section_id,
                "articles": articles,
                "toc": toc,
                "page_name": "{}".format(doc_section_id.name),
                "available_versions": available_versions,
                "current_version": current_version,
                "current_version_name": current_version_name,
                "versioning_option": versioning_option,
                "url_main": "docstokenmulti",
                "section_safe_name": False,
            }
            res = request.render("documentation_builder.documentation", values)
        return res

    @http.route(["/docstokenmulti/<int:doc_version_id>/<int:doc_section_id>"], type="http", auth="public", website=True,
        sitemap=True)
    def documentation_section_version_token(self, doc_version_id=None, doc_section_id=None, **kw):
        """
        The route to open specified documentation section
        """
        doc_section_id = request.env["documentation.section"].sudo().browse(doc_section_id)
        if not doc_section_id or not doc_section_id.exists() or not kw.get("access_token") \
                or not consteq(doc_section_id.access_token, kw.get("access_token")):
            res = request.render("http_routing.404")
        versioning_option = request.env.user.has_group("documentation_builder.group_documentation_versioning")
        res = False
        if not versioning_option or not doc_version_id:
            # if versioning is not turned on or its is zero (global)
            res = request.redirect("/doctoken/{}?{}".format(doc_section_id.id, url_encode(kw)))
        else:
            kw.update({"version_id": doc_version_id})
            res = self.documentation_section_token(docint=doc_section_id.id, **kw)
        return res

    @http.route(['/docs/<int:doc_version_id>/<model("documentation.section"):doc_section_id>/download/<aname>',], 
        type="http", auth="public", website=True, sitemap=False)
    def documentation_section_articles_print(self, doc_version_id=None, doc_section_id=None, aname=None, **kw):
        """
        The route to make and download printing version of the documentation

        Methods:
         * _check_docs_kms_options
         * _print_section_articles
         * get_access_method of documentation.section
         * render_qweb_pdf of report
         * make_response of odoo.request
        """
        res = self._check_docs_kms_options()
        if not res:
            if doc_section_id:
                printed_articles = request.env["knowsystem.article"]
                versioning_option = request.env.user.has_group("documentation_builder.group_documentation_versioning")
                for article_id in doc_section_id.article_ids:
                    if not versioning_option or not article_id.sudo().version_ids \
                            or doc_version_id in article_id.sudo().version_ids.ids:
                        if doc_section_id.get_access_method(article_id, "read", request.website) == "sudo":
                            printed_articles += article_id.with_context(docu_builder=True).sudo().article_id
                res = self._print_section_articles(printed_articles)
            else:
                res = request.render("http_routing.404")
        return res

    @http.route(["/docs/<model('documentation.section'):doc_section_id>/download/<aname>"], type="http", auth="public",
        website=True, sitemap=False)
    def documentation_section_no_version_articles_print(self, doc_section_id=None, aname=None, **kw):
        """
        The route to make and download printing version of the documentation

        Methods:
         * _check_docs_kms_options
         * get_access_method of documentation.section
         * _print_section_articles
         * render_qweb_pdf of report
         * make_response of odoo.request
        """
        res = self._check_docs_kms_options()
        doc_version_id = False
        if not res:
            if doc_section_id:
                printed_articles = request.env["knowsystem.article"]
                versioning_option = request.env.user.has_group("documentation_builder.group_documentation_versioning")
                for article_id in doc_section_id.article_ids:
                    if not versioning_option or not article_id.sudo().version_ids \
                            or doc_version_id in article_id.sudo().version_ids.ids:
                        if doc_section_id.get_access_method(article_id, "read", request.website) == "sudo":
                            printed_articles += article_id.with_context(docu_builder=True).sudo().article_id
                res = self._print_section_articles(printed_articles)
            else:
                res = request.render("http_routing.404")
        return res
