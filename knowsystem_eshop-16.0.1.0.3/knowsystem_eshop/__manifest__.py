# -*- coding: utf-8 -*-
{
    "name": "KnowSystem: eCommerce",
    "version": "16.0.1.0.3",
    "category": "eCommerce",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/knowsystem-ecommerce-722",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "website_sale",
        "knowsystem_website"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/res_config_settings.xml",
        "views/product_template.xml",
        "views/product_attribute.xml",
        "views/templates.xml"
    ],
    "assets": {
        "web.assets_frontend": [
                "knowsystem_eshop/static/src/knowsystem_faq/*.js",
                "knowsystem_eshop/static/src/knowsystem_faq/*.scss",
                "knowsystem_eshop/static/src/knowsystem_faq/*.xml"
        ]
},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to prepare FAQs/documentation for Odoo eCommerce product pages. Product FAQs. Product instructions. Product documentation. Product guidelines. Products FAQs. Products instructions. Products documentation. Products guidelines. E-shop FAQs. E-shop instructions. E-shop guidelines. E-commerce FAQs. E-commerce  instructions. E-commerce  guidelines.",
    "description": """For the full details look at static/description/index.html
* Features * 
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "28.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=143&ticket_version=16.0&url_type_id=3",
}