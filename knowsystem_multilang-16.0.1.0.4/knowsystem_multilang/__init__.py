# -*- coding: utf-8 -*-

from . import models
from . import controllers
from . import reports
from . import wizard

from odoo import api, SUPERUSER_ID

def uninstall_hook(cr, registry):
    """
    The hook to update the core module to convert field translation if needed
    
    To-do:
     * should be removed (including manifest) as soon as the fix is released
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    kms_id = env["ir.module.module"].search([
        ("name", "=", "knowsystem"), ("state", "in", ["installed", "to upgrade", "to install"])
    ], limit=1)
    if kms_id:
        kms_id.button_upgrade()
