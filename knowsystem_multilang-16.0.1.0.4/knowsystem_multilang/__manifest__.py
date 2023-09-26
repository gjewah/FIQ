# -*- coding: utf-8 -*-
{
    "name": "KnowSystem: Multi Languages",
    "version": "16.0.1.0.4",
    "category": "Extra Tools",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/knowsystem-multi-languages-725",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "knowsystem"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/article_copy_language.xml",
        "views/knowsystem_article.xml",
        "views/knowsystem_article_template.xml",
        "views/knowsystem_article_revision.xml"
    ],
    "assets": {
        "web.assets_backend": [
                "knowsystem_multilang/static/src/views/**/*.xml",
                "knowsystem_multilang/static/src/views/**/*.js"
        ]
},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The extension to KnowSystem to translate articles",
    "description": """For the full details look at static/description/index.html
* Features * 
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "10.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=85&ticket_version=16.0&url_type_id=3",
}