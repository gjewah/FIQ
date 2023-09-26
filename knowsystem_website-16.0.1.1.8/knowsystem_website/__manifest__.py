# -*- coding: utf-8 -*-
{
    "name": "KnowSystem: Website and Portal",
    "version": "16.0.1.1.8",
    "category": "Website",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/knowsystem-website-and-portal-720",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "knowsystem",
        "website"
    ],
    "data": [
        "data/data.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/knowsystem_article.xml",
        "views/knowsystem_tag.xml",
        "views/knowsystem_section.xml",
        "views/res_partner.xml",
        "views/templates.xml",
        "views/res_config_settings.xml"
    ],
    "assets": {
        "web.assets_backend": [
                "knowsystem_website/static/src/views/**/*.js"
        ],
        "web.assets_frontend": [
                "knowsystem_website/static/src/scss/knowsystem.scss",
                "knowsystem_website/static/src/js/sections.js"
        ],
        "website.assets_editor": [
                "knowsystem_website/static/src/systray_items/*.js"
        ]
},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The extension to KnowSystem to publish articles to portal and public users",
    "description": """For the full details look at static/description/index.html
* Features * 
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "34.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=84&ticket_version=16.0&url_type_id=3",
}