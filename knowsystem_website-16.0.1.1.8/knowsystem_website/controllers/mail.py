# -*- coding: utf-8 -*-

import werkzeug
from werkzeug import urls

from odoo.http import request
from odoo.addons.mail.controllers.mail import MailController
from odoo.exceptions import AccessError


class MailController(MailController):
    """
    Re-write to manae own access rights for knowsystem.article
    """
    @classmethod
    def _redirect_to_record(cls, model, res_id, access_token=None, **kwargs):
        """
        Re-write to pass access token to be checked to the portal controller
        """
        if model in ["knowsystem.article", "documentation.section"]:
            record_sudo = request.env[model].sudo().browse(res_id).exists()
            if record_sudo.access_token and access_token:
                record_action = record_sudo._get_access_action(force_website=True)
                if record_action["type"] == "ir.actions.act_url":
                    url = record_action["url"]
                    url = urls.url_parse(url)
                    url_params = url.decode_query()
                    url_params["access_token"] = access_token
                    urlreplace = model == "knowsystem.article" and "/knowtoken/{}".format(record_sudo.id) \
                       or "/doctoken/{}".format(record_sudo.id)
                    urlreplace = urls.url_parse(urlreplace)
                    url = urlreplace.replace(query=urls.url_encode(url_params)).to_url()
                    return werkzeug.utils.redirect(url)
        return super(MailController, cls)._redirect_to_record(model, res_id, access_token=access_token)
