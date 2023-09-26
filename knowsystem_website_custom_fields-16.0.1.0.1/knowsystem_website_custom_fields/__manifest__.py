# -*- coding: utf-8 -*-
{
    "name": "KnowSystem: Custom Fields for Website and Portal",
    "version": "16.0.1.0.1",
    "category": "Website",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/knowsystem-custom-fields-for-website-and-portal-724",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "knowsystem_website",
        "knowsystem_custom_fields"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/data.xml",
        "views/knowsystem_article_template.xml",
        "views/article_custom_type.xml"
    ],
    "assets": {},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The extension to KnowSystem to show custom fields for articles' website and portal pages",
    "description": """For the full details look at static/description/index.html
* Features * 
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "0.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=118&ticket_version=16.0&url_type_id=3",
}