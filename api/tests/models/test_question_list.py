# myapp/tests.py

from django.test import TestCase
from api.models import Product, QuestionList


class QuestionListTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Sample Product",
            attributes={"color": "red", "size": "medium"}
        )

        self.product2 = Product.objects.create(
            title="Sample Product 2",
            attributes={"color": "red", "size": "medium"}
        )

        self.question_list = QuestionList.objects.create(
            product=self.product,
            question_list=[
                "question 1", "question 2"
            ]
        )

    def test_question_list_str(self):
        self.assertEqual(str(self.question_list), "Sample Product")

    def test_question_list_attributes(self):
        self.assertEqual(self.question_list.question_list, [
                "question 1", "question 2"
            ])

    def test_question_list_product_relationship(self):
        self.assertEqual(self.question_list.product, self.product)

    def test_blank_question_list(self):
        blank_question_list = QuestionList.objects.create(product=self.product2)
        self.assertEqual(blank_question_list.question_list, [])

    def test_null_question_list(self):
        null_question_list = QuestionList.objects.create(product=self.product2, question_list=None)
        self.assertIsNone(null_question_list.question_list)
