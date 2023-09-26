# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


{
    "name": "Cetmix Unique Product Sequence",
    "version": "16.0.1.0.0",
    "author": "Cetmix",
    "website": "https://cetmix.com",
    "license": "AGPL-3",
    "category": "Product",
    "depends": ["product"],
    "data": [
        "data/product_sequence.xml",
        "views/product_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
