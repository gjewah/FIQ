# -*- coding: utf-8 -*-

from odoo import api, fields, models


class knowsystem_article_template(models.Model):
    """
    The model to keep default articles structures
    """
    _name = "knowsystem.article.template"
    _description = "Article Template"

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

    @api.depends("create_uid")
    def _compute_stable(self):
        """
        Compute method for stable
        The method defines whether the article has been already created and it is fine to make certain operations
        """
        for template in self:
            template.stable = template.create_uid and True or False

    name = fields.Char(string="Name", required=True, translate=False)
    description = fields.Html(string="Article", translate=False, sanitize=False)
    description_arch = fields.Html(string="Body", translate=False, sanitize=False)
    editor_type = fields.Selection(_selection_editor_types, string="Editor Type", default=_default_editor_type)
    stable = fields.Boolean(string="Temporary", compute=_compute_stable)
    active = fields.Boolean(string="Active", default=True)
    sequence = fields.Integer(string="Sequence")
