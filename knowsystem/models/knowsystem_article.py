# -*- coding: utf-8 -*-

import base64
import json
import logging

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.tools import mail
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)

REVISIONCHANGES = {"name", "description", "section_id", "tag_ids", "attachment_ids", "kanban_manual_description"}
SHORTSYMBOLS = 800


class knowsystem_article(models.Model):
    """
    The core model of the tool - to manage knowledge base contents
    """
    _name = "knowsystem.article"
    _inherit = ["mail.activity.mixin", "mail.thread"]
    _description = "Article"
    _mail_post_access = "read"

    @api.model
    def _selection_editor_types(self):
        """
        Return all available editor types

        Returns:
         * list of typles 
        """
        return [("backend_editor", _("Backend Builder")), ("html", _("HTML")), ("text", _("Text"))]

    @api.model
    def _default_editor_type(self):
        """
        Default method for editor_type

        Returns:
         * char
        """
        return self.env["ir.config_parameter"].sudo().get_param("knowsystem_editor_type", "backend_editor")

    @api.depends("revision_ids")
    def _compute_contributor_ids(self):
        """
        Compute method for contributor_ids
        """
        for article in self:
            if article.revision_ids:
                revision_ids = article.revision_ids
                article.write_revision_date = revision_ids[0].change_datetime
                article.write_revision_uid = revision_ids[0].author_id
                contributors = revision_ids.mapped("author_id.id")
                article.contributor_ids = [(6, 0, contributors)]

    def _compute_internal_url(self):
        """
        Compute method for internal_url
        """
        for article in self:
            base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            action_id = self.sudo().env.ref("knowsystem.knowsystem_article_action").id
            menu_id = self.sudo().env.ref("knowsystem.menu_knowsystem_articles").id
            url = "{base}/web#id={id}&action={action}&model=knowsystem.article&view_type=form&menu_id={menu}".format(
                base=base_url, id=article.id, action=action_id, menu=menu_id)
            article.internal_url = url

    def _compute_this_user_favorite(self):
        """
        Compute method for this_user_favorite
        """
        current_user = self.env.user
        for article in self:
            article.this_user_favorite = current_user in article.favourite_user_ids

    @api.depends("like_user_ids")
    def _compute_likes_number(self):
        """
        Compute method for likes_number
        """
        for article in self:
            article.likes_number = len(article.like_user_ids)

    @api.depends("dislike_user_ids")
    def _compute_dislikes_number(self):
        """
        Compute method for dislikes_number
        """
        for article in self:
            article.dislikes_number = len(article.dislike_user_ids)

    @api.depends("like_user_ids", "dislike_user_ids")
    def _compute_this_user_like_state(self):
        """
        Compute method for this_user_like_state
        """
        current_user = self.env.user.id
        for article in self:
            this_user_like_state = False
            if current_user in article.sudo().like_user_ids.ids:
                this_user_like_state = "like"
            elif current_user in article.sudo().dislike_user_ids.ids:
                this_user_like_state = "dislike"
            article.this_user_like_state = this_user_like_state

    @api.depends("like_user_ids", "dislike_user_ids")
    def _compute_likes_score(self):
        """
        Compute method for likes_score
        """
        for article in self:
            article.likes_score = article.likes_number - article.dislikes_number

    @api.depends("user_group_ids", "user_group_ids.users")
    def _compute_access_user_ids(self):
        """
        Compute method for access_user_ids
        """
        for article in self:
            users = article.user_group_ids.mapped("users")
            article.access_user_ids = [(6, 0, users.ids)]

    @api.depends("edit_user_group_ids", "edit_user_group_ids.users")
    def _compute_edit_access_user_ids(self):
        """
        Compute method for edit_access_user_ids
        """
        for article in self:
            users = article.edit_user_group_ids.mapped("users")
            article.edit_access_user_ids = [(6, 0, users.ids)]

    @api.depends("create_uid")
    def _compute_stable(self):
        """
        Compute method for stable
        The method defines whether the article has been already created and it is fine to make certain operations
        """
        for article in self:
            article.stable = article.create_uid and True or False

    def _inverse_name(self):
        """
        The inverse method for name and published_name
        The idea is to have proper criteria for searching and sorting articles in portal / website
        """
        for article in self:
            article.search_name_key = article.published_name or article.name 

    def _inverse_description(self):
        """
        The inverse method for description to prepared indexed contents

        Methods:
         * html2plaintext
         * _shortify_indexed_description
        """
        for article in self:
            indexed_description = ""
            if article.description:
                indexed_description = mail.html2plaintext(article.description)
                indexed_description = "\n".join([s for s in indexed_description.splitlines() if s])
            article.indexed_description = indexed_description
            if not article.kanban_manual_description:
                article.kanban_description = article._shortify_indexed_description()

    def _inverse_kanban_manual_description(self):
        """
        Inverse method for kanban_manual_description

        Methods:
         * _shortify_indexed_description
        """
        for article in self:
            kanban_manual_description = article.kanban_manual_description
            if kanban_manual_description:
                article.kanban_description = kanban_manual_description
            else:
                article.kanban_description = article._shortify_indexed_description()

    def _inverse_attachment_ids(self):
        """
        Inverse method for attachment_ids to make them available for public and portal

        Methods:
         * generate_access_token - of ir.attachment
        """
        for article in self:
            no_token_attachments = article.attachment_ids
            no_token_attachments.write({"res_id": article.id})
            no_token_attachments.generate_access_token()

    @api.model
    def _generate_order_by_inner(self, alias, order_spec, query, reverse_direction=False, seen=None):
        """
        Overwrite to pass context needed for _inherits_join_calc
        """
        return super(knowsystem_article, self.with_context(kms_order_by=True))._generate_order_by_inner(
            alias=alias, order_spec=order_spec, query=query, reverse_direction=reverse_direction, seen=seen
        )

    @api.model
    def _inherits_join_calc(self, alias, fname, query):
        """
        Overwrite to lovercase search
        """
        if self._context.get("kms_order_by") and fname in ["name", "search_name_key"]:
            field = self._fields[fname]
            if field.translate:
                lang = self.env.lang or "en_US"
                if lang == "en_US":
                    return f'LOWER("{alias}"."{fname}"->>\'en_US\')'
                return f'COALESCE(LOWER("{alias}"."{fname}"->>\'{lang}\'), LOWER("{alias}"."{fname}"->>\'en_US\'))'
            else:
                return '"%s"."%s"' % (alias, fname)
        return super(knowsystem_article, self)._inherits_join_calc(alias=alias, fname=fname, query=query)

    name = fields.Char(string="Article Title", required=True, translate=False, inverse=_inverse_name)
    published_name = fields.Char(
        string="Published Title",
        translate=False,
        help="If defined, this title will be used for printed versions, portal articles, and documentation sections",
        inverse=_inverse_name,
    )
    search_name_key = fields.Char(string="Search in title", translate=False, index=True)
    editor_type = fields.Selection(_selection_editor_types, string="Editor Type", default=_default_editor_type)
    description = fields.Html(string="Article", translate=False, sanitize=False, inverse=_inverse_description)
    description_arch = fields.Html(string="Body", translate=False, sanitize=False)
    indexed_description = fields.Text(string="Indexed Article", translate=False)
    kanban_description = fields.Text(string="Summary", translate=False)
    kanban_manual_description = fields.Html(
        string="Preview Summary",
        inverse=_inverse_kanban_manual_description,
        translate=False,
        sanitize=False,
    )
    section_id = fields.Many2one("knowsystem.section", string="Section", ondelete="restrict", index=True)
    tag_ids = fields.Many2many(
        "knowsystem.tag",
        "knowsystem_tag_know_system_article_r_table",
        "knowsystem_tag_r_id",
        "knowsystem_atricle_r_id",
        string="Tags",
        copy=True,
    )
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "knowsystem_article_ir_attachment_rel",
        "knowsystem_article_id",
        "attachment_id",
        string="Attachments",
        copy=True,
        inverse=_inverse_attachment_ids,
    )
    revision_ids = fields.One2many( "knowsystem.article.revision", "article_id", string="Revisions")
    write_revision_date = fields.Datetime(string="Last revision on", compute=_compute_contributor_ids, store=True)
    write_revision_uid = fields.Many2one(
        "res.users",
        string="Last revision by",
        compute=_compute_contributor_ids,
        store=True,
    )
    contributor_ids = fields.Many2many(
        "res.users",
        "res_users_knowsystem_article_rel_contributor_table",
        "res_users_contributor_id",
        "knowsystem_article_contributor_id",
        string="Contributors",
        compute=_compute_contributor_ids,
        store=True,
        help="Users who have created or updated this article",
    )
    internal_url = fields.Char(string="Internal link", compute=_compute_internal_url, store=False, copy=False)
    views_number_internal = fields.Integer(
        string="Views",
        default=0,
        copy=False,
        help="How many times this article has been opened",
    )
    used_in_email_compose = fields.Integer(
        string="Referred in emails",
        default=0,
        copy=False,
        help="How many times this article is used in emails",
    )
    view_stat_ids = fields.Many2many(
        "know.view.stat",
        "know_view_stat_knowsystem_article_rel_table",
        "know_view_stat_id",
        "knowsystem_article_id",
        string="View Stats",
    )
    favourite_user_ids = fields.Many2many(
        "res.users",
        "res_users_knowsystem_article_rel_favor_table",
        "res_users_favor_id",
        "knowsystem_article_favor_id",
        string="Favorite of",
        copy=False,
    )
    this_user_favorite = fields.Boolean(
        string="This user favorite",
        compute=_compute_this_user_favorite,
    )
    like_user_ids = fields.Many2many(
        "res.users",
        "res_users_knowsystem_article_rel_likes_table",
        "res_users_like_id",
        "knowsystem_article_like_id",
        string="Likes by",
        copy=False,
    )
    likes_number = fields.Integer(
        string="Likes Number",
        compute=_compute_likes_number,
        compute_sudo=True,
        store=True,
        default=0,
    )
    dislike_user_ids = fields.Many2many(
        "res.users",
        "res_users_knowsystem_article_rel_dislikes_table",
        "res_users_dislike_id",
        "knowsystem_article_dislike_id",
        string="Dislikes by",
        copy=False,
    )
    dislikes_number = fields.Integer(
        string="Dislikes Number",
        compute=_compute_dislikes_number,
        compute_sudo=True,
        store=True,
        default=0,
    )
    this_user_like_state = fields.Selection(
        [("like", "Liked"), ("dislike", "Disliked")],
        string="Users Like State",
        compute=_compute_this_user_like_state,
    )
    likes_score = fields.Integer(
        string="Likes Score",
        compute=_compute_likes_score,
        compute_sudo=True,
        store=True,
    )
    user_group_ids = fields.Many2many(
        "res.groups",
        "res_groups_knowsystem_article_rel_table",
        "res_groups_id",
        "knowsystem_article_id",
        string="Read access groups",
        help="""If selected, a user should belong to one of those groups to access this article.
The exceptions are (1) KnowSystem administrators; (2) Authors of the articles.
To access the article a user should also have an access to its section""",
    )
    edit_user_group_ids = fields.Many2many(
        "res.groups",
        "res_groups_knowsystem_article_edit_rel_table",
        "res_groups_id",
        "knowsystem_article_id",
        string="Update access groups",
        help="""If selected, a user should belong to one of those groups to be able to edit this article.
The exception is KnowSystem administrators who can edit any article.
To edit this article a user should also be able to edit its section""",
    )
    access_user_ids = fields.Many2many(
        "res.users",
        "res_users_knowsystem_article_rel_table",
        "res_users_id",
        "knowsystem_article_id",
        string="Access Users",
        compute=_compute_access_user_ids,
        compute_sudo=True,
        store=True,
    )
    edit_access_user_ids = fields.Many2many(
        "res.users",
        "res_users_knowsystem_article_edit_rel_table",
        "res_users_id",
        "knowsystem_article_id",
        string="Update Access Users",
        compute=_compute_edit_access_user_ids,
        compute_sudo=True,
        store=True,
    )
    color = fields.Integer(string="Color")
    active_till = fields.Date(string="Active till", help="The article will be auto-archive after this date")
    active = fields.Boolean(string="Active", default=True, copy=False)
    stable = fields.Boolean(string="Temporary", compute=_compute_stable)

    _order = "views_number_internal DESC, id"

    @api.model_create_multi
    def create(self, vals_list):
        """
        Re-write to save this article version in revisions

        Methods:
         * _update_description_safe
         * _prepare_revisions
        """
        new_vals_list = []
        for values in vals_list:
            updated_values = self._update_description_safe(values)
            new_vals_list.append(updated_values)
        res = super(knowsystem_article, self).create(new_vals_list)   
        res._prepare_revisions()
        return res

    def write(self, values):
        """
        Re-write to save this article version in revisions and notify of those

        Methods:
         * _update_description_safe
         * _prepare_revisions
         * _notify_of_revisions
        """
        res = True
        for article in self:
            new_values = article._update_description_safe(values)
            if new_values:
                need_revision = REVISIONCHANGES & set(new_values.keys())
                res = super(knowsystem_article, article).write(new_values)
                if need_revision:
                    # 2
                    self._prepare_revisions()
                    self._notify_of_revisions()
        return res

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        """
        Re-write to add 'copy' in the title
        """
        if default is None:
            default = {}
        if not default.get("name"):
            default["name"] = _("%s (copy)") % (self.name)
        return super(knowsystem_article, self).copy(default)

    ####################################################################################################################
    ####################################### jsTree/navigation/manager actions###########################################
    ####################################################################################################################
    @api.model
    def action_get_hierarchy(self, key):
        """
        The method to prepare hierarchy
        
        Args:
         * key - string - js tree reference

        Methods:
         * _return_nodes of knowsystem.node
         * action_return_types

        Returns:
         * list
        """
        result = []
        if key == "sections":
            result = self.env["knowsystem.section"]._return_nodes()
        elif key == "tags":
            result = self.env["knowsystem.tag"]._return_nodes()
        elif key == "types":
            result = self.action_return_types()
        return result

    @api.model
    def action_return_types(self, website_published=False, website_id=False):
        """
        The method to return article types if they exist (to be overwritten in knowsystem custom fields)
        """
        return False

    @api.model
    def action_create_node(self, model_name, data):
        """
        The method to force node unlinking

        Args:
         * key - string
         * data - dict of node params

        Methods:
         * update_node of password.node

        Returns:
         * int
        """
        node_id = False
        if model_name:
            node_id = self.env[model_name].create_node(data)
        return node_id

    @api.model
    def action_update_node(self, model_name, node_id, data, position):
        """
        The method to force node unlinking

        Args:
         * key - string
         * node_id - int - object ID
         * data - dict of node params
         * position - int or False

        Methods:
         * update_node of password.node
        """
        if model_name:
            node_object = self.env[model_name].browse(node_id)
            if node_object.exists():
                node_object.update_node(data, position)

    @api.model
    def action_delete_node(self, model_name, node_id):
        """
        The method to force node unlinking

        Args:
         * key - string
         * node_id - int - object ID

        Methods:
         * delete_node of password.node
        """
        if model_name:
            node_object = self.env[model_name].browse(node_id)
            if node_object.exists():
                node_object.delete_node()

    @api.model
    def action_print_node(self, domain):
        """
        The method to generate pdf of the article

        Args:
         * domain - list - RPR - to search articles

        Methods:
         * action_save_as_pdf

        Returns:
         * action of the report
        """
        articles = self.search(domain)
        if not articles:
            raise ValidationError(_("There are no articles to print"))
        return articles.action_save_as_pdf()

    @api.model
    def action_return_mass_actions(self):
        """
        The method to return available mass actions in js format

        Returns:
         * list of dict
           ** id
           ** name
        """
        result = []
        self = self.sudo()
        Config = self.env["ir.config_parameter"].sudo()
        mass_actions_list = safe_eval(Config.get_param("knowsystem_ir_actions_server_ids", "[]"))
        mass_action_ids = self.env["ir.actions.server"].search([("id", "in", mass_actions_list)])
        add_to_tour_id = self.sudo().env.ref("knowsystem.knowsystem_article_add_to_tour")
        for mass_action in mass_action_ids:
            if not mass_action.groups_id or (self.env.user.groups_id & mass_action.groups_id):
                if mass_action == add_to_tour_id and not self.env.user.has_group("knowsystem.group_knowsystem_editor"):
                    # add to tour has the special config group, so we check that the user is editor
                    continue
                result.append({"id": mass_action.id, "name": mass_action.name})
        return result

    @api.model
    def action_return_export_conf(self):
        """
        The method to return available mass actions in js format

        Returns:
         * bool
        """
        export_conf = False
        if self.env.is_admin() or self.env.user.has_group("base.group_allow_export"): 
            Config = self.env["ir.config_parameter"].sudo()
            export_conf = safe_eval(Config.get_param("knowsystem_export_option", "False"))
        return export_conf

    @api.model
    def action_proceed_mass_action(self, articles, action_id):
        """
        The method to trigger mass action for selected articles

        Args:
         * articles - list of ints (articles IDs)
         * action_id - int - ir.actions.server id

        Methods:
         * run() of ir.actions.server

        Returns:
         * dict: either action dict, or special view dict, or empty dict if no result

        Extra info:
         * we use api@model with search to make sure each record exists (e.g. deleted in meanwhile)
        """
        article_ids = self.env["knowsystem.article"].with_context(active_test=False).search([("id", "in", articles)])
        result = {}
        if article_ids:
            action_server_id = self.env["ir.actions.server"].browse(action_id)
            if action_server_id.exists():
                action_context = {
                    "active_id": article_ids[0].id,
                    "active_ids": article_ids.ids,
                    "active_model": self._name,
                    "record": article_ids[0],
                    "records": article_ids,
                }
                result = action_server_id.with_context(action_context).run()
                if result and result.get("type"):
                    # introduced not to pass everywhere the default method for articles
                    local_context = {}
                    if result.get("context"):
                        local_context = result.get("context")
                        if not isinstance(local_context, dict):
                            local_context = json.loads(result.get("context"))
                    local_context.update({"default_article_ids": [(6, 0, article_ids.ids)]})
                    result["context"] = local_context
        return result or {}

    def action_save_as_pdf(self):
        """
        The method to generate pdf of the article

        Returns:
         * action of the report
        """
        return self.env.ref("knowsystem.action_report_knowsystem_article").report_action(self)

    ####################################################################################################################
    ####################################### Other actions ##############################################################
    ####################################################################################################################
    def action_get_printed_description(self):
        """
        The method to preprocess description before printing
        Introduced for the case it will be needed
        """
        result = self.description
        result = result.replace("knowsystem_wrapper_td", "knowsystem_wrapper_td knowsystem_wrapper_print_td")
        return result

    @api.model
    def action_get_editor_types(self):
        """
        The method to get all available editor types

        Methods:
         * _selection_editor_types
        """
        return [{"id": etype[0], "name": etype[1]} for etype in self._selection_editor_types()]

    def action_get_published_name(self):
        """
        The method to define what would be used for pubslished article title
        Used for printing version, website/portal views, documentation builder
        
        Extra info:
         * Expected singleton

        Returns:
         * string
        """
        cur_lang = self._context.get("lang") or self.env.user.lang or "en_US"
        self = self.with_context(lang=cur_lang)
        return self.published_name and self.published_name or self.name

    def action_toggle_favorite(self):
        """
        The action to add the article to favourites

        Returns:
         * bool

        Extra info:
         * Expected singleton
        """
        res = True 
        if self.this_user_favorite:
            self.sudo().favourite_user_ids = [(3, self.env.user.id)]
            res = False
        else:
            self.sudo().favourite_user_ids = [(4, self.env.user.id)]
        return res

    def action_like_the_article(self):
        """
        The action to "like" the article

        Returns:
         * tuple: likes/dislikes number/like state

        Extra info:
         * Expected singleton
        """
        current_user = self.env.user.id
        if not self.this_user_like_state == "like":
            if self.this_user_like_state == "dislike":
                self.sudo().dislike_user_ids = [(3, current_user)]
            self.sudo().like_user_ids = [(4, current_user)]
        else:
            self.sudo().like_user_ids = [(3, current_user)]
        return self.likes_number, self.dislikes_number, self.this_user_like_state

    def action_dislike_the_article(self, dislike=False):
        """
        The action to "dislike" the article

        Returns:
         * tuple: likes/dislikes number

        Extra info:
         * Expected singleton
        """
        current_user = self.env.user.id
        if not self.this_user_like_state == "dislike":
            if self.this_user_like_state == "like":
                self.sudo().like_user_ids = [(3, current_user)]
            self.sudo().dislike_user_ids = [(4, current_user)]
        else:
            self.sudo().dislike_user_ids = [(3, current_user)]
        return self.likes_number, self.dislikes_number, self.this_user_like_state

    def action_update_number_of_views(self):
        """
        Increment number of views_number_internal

        Extra info:
         * Expected singleton
        """
        user_id = self._uid
        self = self.sudo()
        self.views_number_internal = self.views_number_internal + 1
        existing_stat_id = self.view_stat_ids.filtered(lambda stat: stat.user_id.id == user_id)
        if existing_stat_id:
            existing_stat_id.counter = existing_stat_id.counter + 1
        else:
            self.view_stat_ids = [(0, 0, {"user_id": user_id, "counter": 1})]

    @api.model
    def action_auto_archive_articles(self):
        """
        The method to find articles set to be auto-archived and make them inactive
        Used for the cron job
        """
        article_ids = self.search([("active_till", "!=", False), ("active_till", "<", fields.Date.today())])
        article_ids.write({"active": False, "active_till": False})

    ####################################################################################################################
    ####################################### Qucik Search & Referencing #################################################
    ####################################################################################################################
    @api.model
    def action_check_option(self, kms_key):
        """
        The method to check whether a quick link should be placed

        Args:
         * kms_key - str - the corresponding ir parameter should be passed (@see res_config_settings)

        Returns:
         * bool
        """
        Config = self.env["ir.config_parameter"].sudo()
        return safe_eval(Config.get_param(kms_key, "False"))

    def action_proceed_article_action(self, action):
        """
        Method to proceed email composer action

        Args:
         * action - char

        Methods:
         * _get_share_url
         * _render_qweb_pdf of ir.actions.reports
         * _update_number_of_used_in_email_compose

        Returns:
         * str (HTML of description or attachments), list of dicts (attachments) or False
        """
        if not self:
            raise ValidationError(_("You have not selected any article"))
        result = False
        self = self.with_context(lang=self.env.user.lang)
        if action == "add":
            result = ""
            for article in self:
                if article.description:
                    # IMPORTANT: id is required for proper sanitizing
                    result += "<div id='knowsystem_style'>{}</div>".format(article.description)
        if action == "share":
            ICPSudo = self.env["ir.config_parameter"].sudo()
            share_type = ICPSudo.get_param("knowsystem_share_link_type", default="internal")
            share_type = share_type == "token" and hasattr(self, "get_portal_url") and "token" \
                or share_type == "website" and hasattr(self, "website_url") and "website" or "internal"
            result = ""
            for article in self:
                if share_type == "token":
                    url = article.get_base_url() + article._get_share_url(redirect=True)
                elif share_type == "website":
                    url = article.website_url
                else:
                    url = article.internal_url
                result += "<p><a href='{}'>{}</a></p>".format(url, article.name)
        elif action == "attach":
            result = []
            common_values = {"res_model": "mail.compose.message", "res_id": 0, "type": "binary"}
            att_vals_list = []
            for article in self:
                result, report_format = self.env["ir.actions.report"]._render_qweb_pdf(
                    "knowsystem.action_report_knowsystem_article", [article.id], {},
                )
                result = base64.b64encode(result)
                att_vals = common_values.copy()
                report_name = "{}.pdf".format(article.action_get_published_name())
                att_vals.update({"name": report_name, "datas": result})
                att_vals_list.append(att_vals)
            attachment_ids = self.env["ir.attachment"].create(att_vals_list)
            result = attachment_ids.read()        
        self._update_number_of_used_in_email_compose()
        return result

    @api.model
    def action_check_quick_creation(self):
        """
        The method to define whether the quick create button should be shown in the activities' list
        """
        result = False
        if self.env.user.has_group("knowsystem.group_knowsystem_editor"):
            ICPSudo = self.env["ir.config_parameter"].sudo()
            result = safe_eval(ICPSudo.get_param("knowsystem_create_from_activities", default="False"))
        return result

    ####################################################################################################################
    ####################################### Helpers ####################################################################
    ####################################################################################################################
    def _update_description_safe(self, values):
        """
        The method to make sure the article description_arch and description are always changed in pair
        The prime use are:
         * importing, when only one of the fields is introduced
         * website, when only one of the fields is actually changed
         * documentation_builder: when one of the field is actually changed while OTHERS might be noted as for a change 

        Methods:
         * _check_update_required

        Returns:
         * dict

        Extra info:
         * Expected singleton or empty recordset
        """
        def make_paired(change_key1, change_key2):
            """
            """
            if updated_values.get(change_key1) is not None and updated_values.get(change_key2) is None:
                if not self or updated_values.get(change_key1) != self[change_key1]:
                    updated_values.update({change_key2: values.get(change_key1)})
                else:
                    updated_values.pop(change_key1)

        updated_values = values.copy()
        make_paired("description_arch", "description")
        make_paired("description", "description_arch")
        return updated_values

    def _prepare_revisions(self):
        """
        The method to save this version of the article before its revisions are saved

        Methods:
         * _prepare_revision_dict
        """
        vals_list = []
        for article in self:
            vals_list.append(article._prepare_revision_dict())
        revision_id = self.env["knowsystem.article.revision"].create(vals_list)

    def _prepare_revision_dict(self):
        """
        The method to prepare this article revision dict
        """
        article = self
        return {
            "article_id": article.id,
            "name": article.name,
            "editor_type": article.editor_type,
            "description": article.description,
            "description_arch": article.description_arch,
            "kanban_manual_description": article.kanban_manual_description,
            "section_id": article.section_id.id,
            "tag_ids": [(6, 0, article.tag_ids.ids)],
            "attachment_ids": [(6, 0, article.attachment_ids.ids)],
        }

    def _notify_of_revisions(self):
        """
        The method to send notifications by detected revisions

        Methods:
         * _render_template_qweb of mail.template (mail.render.mixin)
         * message_post of mail.thread
        """
        for article in self:
            template = self.env.ref("knowsystem.revisions_change_notification")
            body_html = template._render_template_qweb(
                template.body_html, "knowsystem.article", [article.id]
            ).get(article.id)
            subject = template.subject
            article.message_post(body=body_html, subject=subject, subtype_xmlid="knowsystem.mt_knowsystem_revisions")

    def _shortify_indexed_description(self):
        """
        The method to prepare short description based on the indexed description
        
        Returns:
         * str
        
        Extra info:
         * Expected singleton
        """
        ind_descr = self.indexed_description or ""
        return len(ind_descr) >= SHORTSYMBOLS and ind_descr[0:SHORTSYMBOLS] or self.indexed_description or ""

    @api.model
    def _printed_title_in_report(self):
        """
        The method to define whether article titles should be included into the report

        Returns:
         * bool
        """
        ICPSudo = self.env["ir.config_parameter"].sudo()
        knowsystem_no_titles_printed = safe_eval(ICPSudo.get_param("knowsystem_no_titles_printed", default="False"))
        return knowsystem_no_titles_printed        

    def _update_number_of_used_in_email_compose(self):
        """
        Increment number of used_in_email_compose
        """
        for article in self:
            article.sudo().used_in_email_compose = article.sudo().used_in_email_compose + 1
