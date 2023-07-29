# -*- coding: utf-8 -*-

from odoo import fields, models


class add_supplier(models.TransientModel):
    """
    The model to define new supplier details
    """
    _name = "add.supplier"
    _description = "Update Vendors"

    partner_id = fields.Many2one("res.partner", string="Vendor", required=True)
    product_name = fields.Char("Vendor Product Name")
    product_code = fields.Char("Vendor Product Code")
    min_qty = fields.Float(string="Quantity")
    delay = fields.Integer(string="Delivery Lead Time")
    price = fields.Float("Price", default=0.0, digits="Product Price")
    currency_id = fields.Many2one(
        "res.currency",
        "Currency",
        default=lambda self: self.env.company.currency_id.id,
    )
    date_start = fields.Date("Start Date")
    date_end = fields.Date("End Date")

    def action_apply_changes(self):
        """
        The method to prepare new vals for suppliers

        Args:
         * product_ids - product.template recordset
        """
        if self._context.get("active_model") and self._context.get("active_ids") and self.partner_id:
            product_ids = self.env[self._context["active_model"]].browse(self._context["active_ids"])
            seller_ids = product_ids.mapped("seller_ids")
            if seller_ids:
                # to make sure existing seller_ids has higher priority then newly created
                seller_to_high_priority = seller_ids.filtered(lambda sel: sel.sequence <= 0)
                if seller_to_high_priority:
                    seller_to_high_priority.write({"sequence": 1})
            supplier_info_dict = {
                "partner_id": self.partner_id.id,
                "product_name": self.product_name,
                "product_code": self.product_code,
                "min_qty": self.min_qty,
                "delay": self.delay,
                "price": self.price,
                "currency_id": self.currency_id.id,
                "date_start": self.date_start,
                "date_end": self.date_end,
                "sequence": 0,
            }
            values = {"seller_ids": [(0, 0, supplier_info_dict)],}
            product_ids.write(values)
