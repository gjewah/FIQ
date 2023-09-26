# -*- coding: utf-8 -*-

from odoo import fields, models


class create_from_template(models.TransientModel):
    """
    The wizard to create an article template based on some article
    """
    _name = "create.from.template"
    _description = "Create From Template"

    template_id = fields.Many2one("knowsystem.article.template", string="Template", required=True)

    def action_create_from_template(self):
        """
        The method to open new article form with structured from template description

        Extra info:
         * Expected singleton
        """
        action_id = self.sudo().env.ref("knowsystem.knowsystem_article_action_form_only")
        action = action_id.read()[0]
        action["context"] = {
            "default_editor_type": self.template_id.editor_type,
            "default_description": self.template_id.description,
            "default_description_arch": self.template_id.description_arch,
        }
        return action
