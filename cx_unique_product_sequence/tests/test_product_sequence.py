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
        self.product_template = self.env["product.template"]

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

    def test_product_template(self):
        """Tests the product template's unique code sync with variants.

        This test does the following:

        - Creates a new product template
        - Checks the initial variant's code matches the template
        - Creates a second variant
        - Checks the template code does not change
        - Archives the initial variant
        - Checks the template code updates to match the active variant
        """
        # Create a product template
        template = self.product_template.create({"name": "Test Template"})
        # Check the related product
        related_product = template.product_variant_ids[0]
        self.assertTrue(related_product)
        # Check the related product's cx_unique_product_code
        #  is the same as the template's cx_template_product_code
        self.assertEqual(
            template.cx_template_product_code,
            related_product.cx_unique_product_code,
            "code should be the same",
        )
        # Create another related product.product.
        related_product_1 = self.product_product.create(
            {
                "name": "Test Product 1",
                "product_tmpl_id": template.id,
            }
        )
        self.assertTrue(related_product_1)
        # Check if the  template's cx_template_product_code has not changed
        self.assertEqual(
            template.cx_template_product_code,
            related_product.cx_unique_product_code,
            "code should not change",
        )
        # Archive the first related product.product.
        related_product.active = False
        # Check if the  template's cx_template_product_code has changed
        self.assertEqual(
            template.cx_template_product_code,
            related_product_1.cx_unique_product_code,
            "code should be equal to code of next active product.product",
        )
