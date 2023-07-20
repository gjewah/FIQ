# -*- coding: utf-8 -*-
{
    "name": "Mass Vendors Update",
    "version": "16.0.1.0.1",
    "category": "Purchases",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/mass-vendors-update-768",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "product",
        "purchase"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "wizard/add_supplier_view.xml"
    ],
    "assets": {},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to add suppliers to a number of Odoo products simultaneously",
    "description": """For the full details look at static/description/index.html
- More actions on product templates are introduced by the tool &lt;a href=&#39;https://apps.odoo.com/apps/modules/16.0/product_management/&#39;&gt;Product Management Interface&lt;/a&gt;
* Features * 
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "14.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=35&ticket_version=16.0&url_type_id=3",
}