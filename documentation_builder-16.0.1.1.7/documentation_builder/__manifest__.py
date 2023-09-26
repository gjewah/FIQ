# -*- coding: utf-8 -*-
{
    "name": "Odoo Documentation Builder",
    "version": "16.0.1.1.7",
    "category": "Website",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/odoo-documentation-builder-721",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "knowsystem_website"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/res_config_settings.xml",
        "views/documentation_section.xml",
        "views/documentation_category.xml",
        "views/documentation_version.xml",
        "views/knowsystem_article.xml",
        "wizard/add_to_documentation.xml",
        "views/templates.xml",
        "views/menu.xml"
    ],
    "assets": {
        "web.assets_frontend": [
                "documentation_builder/static/src/scss/documentation.scss",
                "documentation_builder/static/src/js/documentation.js"
        ]
},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to create website documentation based on your knowledge base. Portal documentation. Partner documentation. Product documentation. Create documentation. KMS. Knowledge management. Help documentation. Documentation online.",
    "description": """For the full details look at static/description/index.html
* Features * 
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "98.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=137&ticket_version=16.0&url_type_id=3",
}