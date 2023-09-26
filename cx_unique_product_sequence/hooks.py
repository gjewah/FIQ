# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID, api

SEQUENCE_START = 1000001


def post_init_hook(cr, registry):
    """ """
    env = api.Environment(cr, SUPERUSER_ID, {})

    products = env["product.product"].search(
        [
            "|",
            ("cx_unique_product_code", "=", False),
            ("cx_unique_product_code", "=", "/"),
        ]
    )  # Retrieve all matching products

    # Start the counter for generating unique values

    for index, product in enumerate(products, start=SEQUENCE_START):
        product.cx_unique_product_code = str(index)

    # Update the sequence with the next value
    sequence = (
        env["ir.sequence"].sudo().search([("code", "=", "product.product.unique")])
    )

    if sequence:
        next_value = len(products) + SEQUENCE_START
        sequence.write({"number_next_actual": next_value})
