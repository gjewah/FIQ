# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class knowsystem_article_revision(models.Model):
    """
    The model to keep previous versions of the article and change data
    """
    _name = "knowsystem.article.revision"
    _description = "Article Revision"

    @api.model
    def _selection_editor_types(self):
        """
        The method to return all available editor types

        Methods:
         * _selection_editor_types of knowsystem.article

        Returns:
         * list of typles
        """
        return self.env["knowsystem.article"]._selection_editor_types()

    @api.model
    def _default_editor_type(self):
        """
        Default method for editor_type

        Methods:
         * _default_editor_type of knowsystem.article

        Returns:
         * char
        """
        return self.env["knowsystem.article"]._default_editor_type()

    def _compute_name_change(self):
        """
        Compute method for name_change, description_change, tags_change, section_change, attachments_change

        Methods:
         * _return_previous_revision_domain
        """
        for revision in self:
            name_change = description_change = tags_change = section_change = attachments_change = False
            kanban_manual_description_change = False
            domain = revision._return_previous_revision_domain()
            previous_revision = self.search(domain, order="change_datetime DESC", limit=1)
            if previous_revision:
                if previous_revision.name != revision.name:
                    name_change = True
                if previous_revision.description != revision.description:
                    description_change = len(revision.description or "") - len(previous_revision.description or "")
                if previous_revision.kanban_manual_description != revision.kanban_manual_description:
                    kanban_manual_description_change = len(revision.kanban_manual_description or "") \
                        - len(previous_revision.kanban_manual_description or "")
                if previous_revision.tag_ids != revision.tag_ids:
                    tags_change = True
                if previous_revision.section_id != revision.section_id:
                    section_change = True
                if previous_revision.attachment_ids != revision.attachment_ids:
                    attachments_change = True
            revision.name_change = name_change
            revision.description_change = description_change
            revision.tags_change = tags_change
            revision.section_change = section_change
            revision.attachments_change = attachments_change
            revision.kanban_manual_description_change = kanban_manual_description_change

    article_id = fields.Many2one("knowsystem.article", string="Article", ondelete="cascade")
    editor_type = fields.Selection(_selection_editor_types, string="Editor Type", default=_default_editor_type)
    name = fields.Char(string="Previous Title", required=True, translate=False)
    description = fields.Html(string="Previous Article", translate=False, sanitize=False)
    description_arch = fields.Html(string="Body", translate=False, sanitize=False)
    kanban_manual_description = fields.Html(string="Preview Summary",translate=False, sanitize=False)
    section_id = fields.Many2one("knowsystem.section", string="Previous Section")
    tag_ids = fields.Many2many(
        "knowsystem.tag",
        "knowsystem_tag_know_system_article_revision_rel_table",
        "knowsystem_tag_id",
        "knowsystem_atricle_revision_id",
        string="Previous Tags",
    )
    author_id = fields.Many2one("res.users", string="Revision author", default=lambda self: self.env.user)
    change_datetime = fields.Datetime(string="Revision date", default=lambda self: fields.Datetime.now())
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "knowsystem_article_revision_ir_attachment_rel",
        "knowsystem_article_revision_id",
        "attachment_id",
        string="Previous Attachments",
    )
    name_change = fields.Boolean(string="Name", compute=_compute_name_change)
    kanban_manual_description_change = fields.Integer(string="Preview", compute=_compute_name_change)
    description_change = fields.Integer(string="Description", compute=_compute_name_change)
    tags_change = fields.Boolean(string="Tags", compute=_compute_name_change)
    section_change = fields.Boolean(string="Section", compute=_compute_name_change)
    attachments_change = fields.Boolean(string="Attachments", compute=_compute_name_change)

    _order = "change_datetime DESC, id"

    def name_get(self):
        """
        Overloading the method, to show revision author
        """
        result = []
        for revision in self:
            name = _("Revision of the article {} by {} on {}".format(
                revision.name,
                revision.author_id.name,
                revision.change_datetime,
            ))
            result.append((revision.id, name))
        return result

    def action_get_revisions(self):
        """
        The method to return revisions in proper format

        Methods:
         * _prepare_revision_dict

        Returns:
         * list of dicts

        Extra info:
         * We check here dict for emptiness for inheritance purposes. For example, not to show different languages
           revisions
        """
        result = []
        for revision in self:
            revision_dict = revision._prepare_revision_dict()
            if revision_dict:
                result.append(revision_dict)
        return result

    def action_recover_this_revision(self):
        """
        The method to return the linked article to this revision state

        Methods:
         * action_back_to_article

        Returns:
         * action

        Extra info:
         * Expected singleton
        """
        self.article_id.write({
            "name": self.name,
            "description_arch": self.description_arch,
            "description": self.description,
            "kanban_manual_description": self.kanban_manual_description,
            "section_id": self.section_id.id,
            "tag_ids": [(6, 0, self.tag_ids.ids)],
            "attachment_ids": [(6, 0, self.attachment_ids.ids)],
        })
        return self.action_back_to_article()

    def action_back_to_article(self):
        """
        The action to return back to article from revision
        """
        action_id = self.sudo().env.ref("knowsystem.knowsystem_article_action_form_only")
        action = action_id.read()[0]
        action["res_id"] = self.article_id.id
        return action
    
    def _prepare_revision_dict(self):
        """
        The method to prepare revision dict
        
        Returns:
         * dict

        Extra info:
         * Expected singleton
        """
        return {
            "id": self.id,
            "author_id": self.author_id.name,
            "change_datetime": self.change_datetime,
            "name": self.name_change and self.name or False,
            "tag_ids": self.tags_change and ", ".join([tag.name for tag in self.tag_ids]) or False,
            "section_id": self.section_change and self.section_id.name or False,
            "description": self.description_change or False,
            "kanban_manual_description": self.kanban_manual_description_change or False,
            "attachment_ids": self.attachments_change \
                and ", ".join([attach.name for attach in self.attachment_ids]) or False,
        }

    def _return_previous_revision_domain(self):
        """
        The method to return the domain to find the previous revision
        Needed for inheritance purposes

        Extra info:
         * Expected singleton
        """
        return [
            ("change_datetime", "<=", self.change_datetime),
            ("id", "!=", self.id),
            ("article_id", "=", self.article_id.id),
        ]
