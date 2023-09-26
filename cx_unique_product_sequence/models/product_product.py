# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    cx_unique_product_code = fields.Char(
        required=True,
        default="/",
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Overrides create() method from product.product model.

        Parameters:
            vals_list (list): List of dicts containing field values to create products.

        Returns:
            res: Result of calling super().create() with updated vals_list."""

        for vals in vals_list:
            product_code = vals.get("cx_unique_product_code")
            if product_code is None or product_code == "/":
                vals.update(
                    {
                        "cx_unique_product_code": self.env["ir.sequence"].next_by_code(
                            "product.product.unique"
                        )
                    }
                )
                return super().create(vals_list)
