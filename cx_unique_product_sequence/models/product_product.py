# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    cx_unique_product_code = fields.Char(
        required=True,
        default="/",
        translate=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Overrides create() method from product.product model.

        Parameters:
            vals_list (list): List of dicts containing field values to create products.

        Returns:
            res: Result of calling super().create() with updated vals_list."""
        vals_list_updated = []
        for vals in vals_list:
            # product_code = vals.get("cx_unique_product_code")
            if (
                "cx_unique_product_code" not in vals
                or vals["cx_unique_product_code"] == "/"
            ):
                vals.update(
                    {
                        "cx_unique_product_code": self.env["ir.sequence"].next_by_code(
                            "product.product.unique"
                        )
                    }
                )
            vals_list_updated.append(vals)

        return super().create(vals_list)

    class ProductTemplate(models.Model):
        _inherit = "product.template"

        cx_template_product_code = fields.Char(
            string="Product Number",
            compute="_compute_related_product_product_code",
            translate=True,
            store=True,
        )

        @api.depends(
            "product_variant_ids.cx_unique_product_code", "product_variant_ids.active"
        )
        def _compute_related_product_product_code(self):
            """Computes related product Product Number."""
            for template in self:
                product = template.product_variant_ids.filtered(lambda p: p.active)
                if product:

                    template.cx_template_product_code = product[
                        0
                    ].cx_unique_product_code
                else:
                    template.cx_template_product_code = "/"
