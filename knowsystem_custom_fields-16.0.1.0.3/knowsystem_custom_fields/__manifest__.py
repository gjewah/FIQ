# -*- coding: utf-8 -*-
{
    "name": "KnowSystem: Custom Fields",
    "version": "16.0.1.0.3",
    "category": "Extra Tools",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/knowsystem-custom-fields-723",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "knowsystem",
        "custom_fields"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/custom_article_fields.xml",
        "views/article_custom_type.xml",
        "views/knowsystem_article.xml",
        "wizard/article_type_update.xml"
    ],
    "assets": {
        "web.assets_qweb": [
                "knowsystem_custom_fields/static/src/xml/*.xml"
        ]
},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The extension to KnowSystem to create custom fields",
    "description": """For the full details look at static/description/index.html
* Features * 
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "20.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=117&ticket_version=16.0&url_type_id=3",
}