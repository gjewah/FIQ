# -*- coding: utf-8 -*-

from odoo import models


class IrHttp(models.AbstractModel):
    """
    Overwrite to add the module to the website translation
    """
    _inherit = "ir.http"

    @classmethod
    def _get_translation_frontend_modules_name(cls):
        """
        Re-write to add the module for the translated modules
        """
        mods = super(IrHttp, cls)._get_translation_frontend_modules_name()
        return mods + ["knowsystem_website"]
