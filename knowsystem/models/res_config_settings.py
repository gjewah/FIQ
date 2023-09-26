# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class res_config_settings(models.TransientModel):
    """
    Overwrite to introduce KnowSystem settings
    """
    _inherit = "res.config.settings"

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

    @api.depends("knowsystem_ir_actions_server_ids_str")
    def _compute_knowsystem_ir_actions_server_default_model_id(self):
        """
        Compute method for knowsystem_ir_actions_server_default_model_id
        """
        knowsystem_model_id = self.env["ir.model"].search([("model", "=", "knowsystem.article")], limit=1).id
        for conf in self:
            conf.knowsystem_ir_actions_server_default_model_id = knowsystem_model_id

    @api.depends("knowsystem_ir_actions_server_ids_str")
    def _compute_knowsystem_ir_actions_server_ids(self):
        """ 
        Compute method for knowsystem_ir_actions_server_ids 
        """
        for setting in self:
            knowsystem_ir_actions_server_ids = []
            if setting.knowsystem_ir_actions_server_ids_str:
                try:
                    actions_list = safe_eval(setting.knowsystem_ir_actions_server_ids_str)
                    knowsystem_ir_actions_server_ids = self.env["ir.actions.server"].search(
                        [("id", "in", actions_list)]
                    ).ids
                except Exception as e:
                    knowsystem_ir_actions_server_ids = []
            setting.knowsystem_ir_actions_server_ids = [(6, 0, knowsystem_ir_actions_server_ids)]

    def _inverse_knowsystem_ir_actions_server_ids(self):
        """
        Inverse method for knowsystem_ir_actions_server_ids
        """
        for setting in self:
            knowsystem_ir_actions_server_ids_str = ""
            if setting.knowsystem_ir_actions_server_ids:
                knowsystem_ir_actions_server_ids_str = "{}".format(setting.knowsystem_ir_actions_server_ids.ids)
            setting.knowsystem_ir_actions_server_ids_str = knowsystem_ir_actions_server_ids_str

    @api.onchange("module_knowsystem_website")
    def _onchange_module_knowsystem_website(self):
        """
        Ohchange method for module_knowsystem_website
        """
        for conf in self:
            if not conf.module_knowsystem_website:
                conf.module_documentation_builder = False
                conf.module_knowsystem_eshop = False
                conf.module_knowsystem_website_custom_fields = False
                conf.knowsystem_share_link_type = "internal"

    @api.onchange("module_knowsystem_custom_fields")
    def _onchange_module_knowsystem_custom_fields(self):
        """
        Onchange method for module_knowsystem_custom_fields
        """
        for conf in self:
            if not conf.module_knowsystem_custom_fields:
                conf.module_knowsystem_website_custom_fields = False

    @api.onchange("external_layout_knowsystem_id")
    def _onchange_external_layout_knowsystem_id(self):
        """
        Onchange method for external_layout_knowsystem_id
        The idea is put default if updated to empty
        """
        standard_id = self.sudo().env.ref("knowsystem.external_layout_knowsystem")
        if standard_id:
            for conf in self:
                if not conf.external_layout_knowsystem_id:
                    conf.external_layout_knowsystem_id = standard_id

    module_knowsystem_multilang = fields.Boolean(string="Multiple Languages")
    module_knowsystem_website = fields.Boolean(string="Publish to portal and website")
    module_documentation_builder = fields.Boolean(string="Documentation Builder")
    module_knowsystem_custom_fields = fields.Boolean(string="Custom fields for articles")
    module_knowsystem_website_custom_fields = fields.Boolean(string="Show custom fields in portal and website")
    module_knowsystem_eshop = fields.Boolean(string="Use for eCommerce FAQ")
    group_knowsystem_tours_option = fields.Boolean(
        string="Learning Tours", 
        implied_group="knowsystem.group_knowsystem_learning_tours",
    )
    knowsystem_editor_type = fields.Selection(
        _selection_editor_types,
        string="Default Editor Type",
        default="backend_editor",
        config_parameter="knowsystem_editor_type",
    )
    knowsystem_models_option = fields.Boolean(
        string="Articles by Documents", 
        config_parameter="knowsystem_models_option",
    )
    knowsystem_composer_option = fields.Boolean(
        string="Articles in Email Composers",
        config_parameter="knowsystem_composer_option",
    )
    knowsystem_activity_option = fields.Boolean(
        string="Articles in Activities",
        config_parameter="knowsystem_activity_option",
    )
    knowsystem_systray_option = fields.Boolean(
        string="Articles in systray",
        config_parameter="knowsystem_systray_option",
    )
    knowsystem_share_link_type = fields.Selection(
        [("internal", "Internal URL")],
        string="Share URL type",
        config_parameter="knowsystem_share_link_type",
        default="internal",
    )
    knowsystem_no_titles_printed = fields.Boolean(
        string="Print without titles",
        config_parameter="knowsystem_no_titles_printed",
    )
    knowsystem_custom_layout = fields.Boolean(related="company_id.knowsystem_custom_layout", readonly=False)
    external_layout_knowsystem_id = fields.Many2one(related="company_id.external_layout_knowsystem_id", readonly=False)
    knowsystem_export_option = fields.Boolean(string="Export articles", config_parameter="knowsystem_export_option")
    knowsystem_create_from_activities = fields.Boolean(
        string="Create from activities",
        config_parameter="knowsystem_create_from_activities",
    )
    knowsystem_ir_actions_server_default_model_id = fields.Many2one(
        "ir.model",
        compute=_compute_knowsystem_ir_actions_server_default_model_id,
        string="Default KMS model"
    )
    knowsystem_ir_actions_server_ids = fields.Many2many(
        "ir.actions.server",
        compute=_compute_knowsystem_ir_actions_server_ids,
        inverse=_inverse_knowsystem_ir_actions_server_ids,
        string="Mass actions",
        domain=[("model_name", "=", "knowsystem.article")],
    )
    knowsystem_ir_actions_server_ids_str = fields.Char(
        string="Mass actions (Str)", 
        config_parameter="knowsystem_ir_actions_server_ids",
    )

    def edit_kms_layout_external_header(self):
        """
        The method to open the basic layout 
        """
        if not self.external_layout_knowsystem_id:
            return False
        view_key = self.external_layout_knowsystem_id.key
        if view_key == "knowsystem.external_layout_knowsystem":
            view_key = "knowsystem.external_layout_knowsystem_custom"
        return self._prepare_report_view_action(view_key)

    def edit_kms_report(self):
        """
        The method to open the report itself
        """
        report_id = self.sudo().env.ref("knowsystem.report_article_document_custom")
        if not report_id:
            return False
        return self._prepare_report_view_action(report_id.key)
    
    def edit_kms_paperformat(self):
        """
        The method to open the report itself
        """
        action_id = self.sudo().env.ref("knowsystem.paper_format_action_knowsystem")
        paperformat_id = self.sudo().env.ref("knowsystem.paperformat_knowsystem")
        if not action_id or not paperformat_id:
            return False
        action_dict = action_id.read()[0]
        action_dict["res_id"] = paperformat_id.id
        return action_dict
