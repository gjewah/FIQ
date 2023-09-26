# -*- coding: utf-8 -*-

from odoo import api, fields, models


class knowsystem_section(models.Model):
    """
    The model to structure articles in sections and subsections
    """
    _name = "knowsystem.section"
    _inherit = ["knowsystem.node"]
    _description = "Section"

    @api.depends(
        "parent_id", "parent_id.access_user_ids", "parent_id.read_global", "user_group_ids", "user_group_ids.users"
    )
    def _compute_access_user_ids(self):
        """
        Compute method for access_user_ids
        """
        self.clear_caches() # to avoid taking parent-related cache and sudden error
        left_section_ids = self
        while left_section_ids:
            root_section_ids = left_section_ids.filtered(lambda fo: fo.parent_id not in left_section_ids)
            for section in root_section_ids:
                this_section_user_group_ids = section.user_group_ids
                # if there are own user groups > it already is not global
                read_global = not this_section_user_group_ids and True or False
                # here we get user that can access this section when neglecting hieratchy
                access_user_ids = this_section_user_group_ids.mapped("users")
                # now check the parent
                parent_section = section.parent_id
                if parent_section:
                    parent_read_global = parent_section.read_global
                    if read_global and not parent_read_global:
                        # this is global, parent is not, so should use parent users
                        access_user_ids = parent_section.access_user_ids
                    elif not read_global and not parent_read_global:
                        # both are not global, so should find the intersection
                        access_user_ids = access_user_ids & parent_section.access_user_ids
                    # a section is global, if it is global itself and its parent is also global
                    read_global = read_global and parent_read_global or False
                section.access_user_ids = [(6, 0, access_user_ids.ids)]
                section.read_global = read_global
            left_section_ids -= root_section_ids 

    @api.depends(
        "parent_id", "parent_id.edit_access_user_ids", "parent_id.edit_global", "edit_user_group_ids", 
        "edit_user_group_ids.users"
    )
    def _compute_edit_access_user_ids(self):
        """
        Compute method for edit_access_user_ids
        """
        self.clear_caches() # to avoid taking parent-related cache and sudden error
        left_section_ids = self
        while left_section_ids:
            root_section_ids = left_section_ids.filtered(lambda fo: fo.parent_id not in left_section_ids)
            for section in root_section_ids:
                this_section_user_group_ids = section.edit_user_group_ids
                # if there are own edit user groups > it already is not global
                edit_global = not this_section_user_group_ids and True or False
                # here we get user that can edit this section when neglecting hieratchy
                edit_access_user_ids = this_section_user_group_ids.mapped("users")
                # now check the parent
                parent_section = section.parent_id
                if parent_section:
                    parent_edit_global = parent_section.edit_global
                    if edit_global and not parent_edit_global:
                        # this is global, parent is not, so should use parent users
                        edit_access_user_ids = parent_section.edit_access_user_ids
                    elif not edit_global and not parent_edit_global:
                        # both are not global, so should find the intersection
                        edit_access_user_ids = edit_access_user_ids & parent_section.edit_access_user_ids
                    # a section is global, if it is global itself and its parent is also global
                    edit_global = edit_global and parent_edit_global or False
                section.edit_access_user_ids = [(6, 0, edit_access_user_ids.ids)]
                section.edit_global = edit_global
            left_section_ids -= root_section_ids 

    parent_id = fields.Many2one("knowsystem.section", string="Parent Section")
    child_ids = fields.One2many("knowsystem.section", "parent_id", string="Sub Sections")
    article_ids = fields.One2many("knowsystem.article", "section_id", string="Articles")
    user_group_ids = fields.Many2many(
        "res.groups",
        "res_groups_knowsystem_section_rel_table",
        "res_groups_id",
        "knowsystem_section_id",
        string="Read access groups",
        help="""If selected, a user should belong to one of those groups to access this section and ALL ITS ARTICLES.
Besides, a user should have rights to the parent sections hierarchically.
The exceptions are (1) KnowSystem administrators; (2) Authors of the articles""",
    )
    edit_user_group_ids = fields.Many2many(
        "res.groups",
        "res_groups_knowsystem_section_edit_rel_table",
        "res_groups_id",
        "knowsystem_section_id",
        string="Update access groups",
        help="""If selected, a user should belong to one of the groups to update this section and ALL ITS ARTICLES.
Besides, a user should have rights to the parent sections hierarchically.
The exception is KnowSystem administrators who can edit any section and article""",
    )
    access_user_ids = fields.Many2many(
        "res.users",
        "res_users_knowsystem_section_rel_table",
        "res_users_id",
        "knowsystem_section_id",
        string="Access Users",
        compute=_compute_access_user_ids,
        compute_sudo=True,
        store=True,
        recursive=True,
    )
    edit_access_user_ids = fields.Many2many(
        "res.users",
        "res_users_knowsystem_section_edit_rel_table",
        "res_users_id",
        "knowsystem_section_id",
        string="Update Access Users",
        compute=_compute_edit_access_user_ids,
        compute_sudo=True,
        store=True,
        recursive=True,
    )
    read_global = fields.Boolean(
        string="Global Read Rights",
        compute=_compute_access_user_ids,
        compute_sudo=True,
        store=True,
        recursive=True,
    )
    edit_global = fields.Boolean(
        string="Global Edit Rights",
        compute=_compute_edit_access_user_ids,
        compute_sudo=True,
        store=True,
        recursive=True,
    )

    _order = "sequence, id"
