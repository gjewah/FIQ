# -*- coding: utf-8 -*-
{
    "name": "Contacts Color Coding",
    "version": "16.0.1.0.4",
    "category": "Extra Tools",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/contacts-color-coding-767",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "base_setup"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/color_code.xml",
        "views/res_partner.xml",
        "views/res_config_settings.xml"
    ],
    "assets": {
        "web.assets_backend": [
                "partner_color_codes/static/src/components/**/*.js",
                "partner_color_codes/static/src/components/**/*.xml",
                "partner_color_codes/static/src/components/**/*.scss",
                "partner_color_codes/static/src/views/**/*.js",
                "partner_color_codes/static/src/views/**/*.xml"
        ]
},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "Partner color coding to score contacts and make rational decisions in any business area. Color codes. Customer scoring. Trusted partners. Highlighted contacts. Blacklist partners. Blacklist customers. Partner scoring. Blacklist. Black list.",
    "description": """For the full details look at static/description/index.html
* Features * 
- Automatic color codes
- Flexible codes classifier
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "98.0",
    "currency": "EUR",
    "post_init_hook": "post_init_hook",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=12&ticket_version=16.0&url_type_id=3",
}