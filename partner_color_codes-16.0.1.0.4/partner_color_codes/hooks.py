# -*- coding: utf-8 -*-

def post_init_hook(cr, registry):
    """
    Hook to create default list of color codes
    """
    from odoo import SUPERUSER_ID, api
    env = api.Environment(cr, SUPERUSER_ID, {})
    color_code = env["color.code"]
    references = ["Black List", "Dangerous", "Top Quality", "Partnership", "Neglected"]
    names = ["#000000", "#ff0000", "#00ff00", "#0000ff", "#707070"]
    sequences = ["0", "10", "20", "30", "50"]
    vals_list = []
    for itera in range(0, 5):
        vals_list.append({"name": names[itera], "reference": references[itera], "sequence": sequences[itera]})
    color_code.sudo().create(vals_list)
