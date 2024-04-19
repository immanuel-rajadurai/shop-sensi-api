from django.core.exceptions import ValidationError
from django.test import TestCase
from api.models import Product

class ProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Sample Product",
            attributes={"color": "red", "size": "medium"}
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Sample Product")

    def test_product_attributes(self):
        self.assertEqual(self.product.attributes, {"color": "red", "size": "medium"})

    def test_unique_title(self):
        with self.assertRaises(Exception):
            Product.objects.create(title="Sample Product", attributes={"color": "blue"})

    def test_blank_attributes(self):
        blank_product = Product.objects.create(title="Blank Product")
        self.assertEqual(blank_product.attributes, {})

    def test_null_attributes(self):
        null_product = Product.objects.create(title="Null Product", attributes=None)
        self.assertIsNone(null_product.attributes)