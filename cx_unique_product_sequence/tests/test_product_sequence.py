# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests.common import TransactionCase, tagged

from ..hooks import post_init_hook


@tagged("post_install", "-at_install")
class TestProductSequence(TransactionCase):
    """Tests for creating product with and without Product Sequence"""

    def setUp(self):
        super(TestProductSequence, self).setUp()
        self.product_product = self.env["product.product"]
        self.sequence = self.env["ir.sequence"]

    def test_post_init_hook(self):
        """Tests the post_init_hook function.

        This test does the following:

        - Creates a new product with a predefined cx_unique_product_code.
        - Updates the cx_unique_product_code to an invalid value.
        - Calls post_init_hook to set right  cx_unique_product_code.
        - Verifies that the cx_unique_product_code was set correctly.

        Args:
            self (TestProductSequence): The test class instance.
        """
        product_3 = self.product_product.create({"name": "Apple"})

        # self.cr.execute(
        #     "update product_product set cx_unique_product_code=NULL where id=%s",
        #     (tuple(product_3.ids),),
        # )
        # Set cx_unique_product_code to '/'
        product_3.write({"cx_unique_product_code": "/"})
        product_3.invalidate_recordset()
        self.assertEqual(product_3.cx_unique_product_code, "/")
        post_init_hook(self.env.cr, None)

        self.assertEqual(
            product_3.cx_unique_product_code,
            "1000001",
            "cx_unique_product_code should be '1000001'",
        )

    def test_product_product_creation(self):
        """Tests creating a new product and validating its unique Product Number.

        This test does the following:

        - Gets the next sequence number for unique Product Numbers.
        - Creates a new product.
        - Validates that the new product's cx_unique_product_code matches
          the expected next sequence number.

        Args:
            self (obj): The test class instance
        """

        next_number = self.sequence.search(
            [("code", "=", "product.product.unique")]
        ).number_next_actual
        product_1 = self.product_product.create({"name": "product 1"})

        self.assertEqual(
            product_1.cx_unique_product_code,
            str(next_number),
            "Product Number should match next sequence number",
        )
