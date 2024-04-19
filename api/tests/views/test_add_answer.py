# Django Rest Framework unit tests for the 'add_answer' view

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Product, QuestionList, AnswerList

class AddAnswerViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(title="Sample Product", attributes={"color": "blue"})
        self.product2 = Product.objects.create(title="Sample Product 2", attributes={"color": "blue"})
        self.question_list = QuestionList.objects.create(product=self.product, question_list=["Q1", "Q2"])
        self.url = "/api/add_answer/"

    def test_add_answer_valid_data(self):
        data = {
            "product_title": "Sample Product",
            "answers": ["A1", "A2"]
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AnswerList.objects.count(), 1)
        self.assertEqual(AnswerList.objects.first().answer_list, ["A1", "A2"])

    def test_add_answer_missing_product_title(self):
        data = {
            "answers": ["A1", "A2"]
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(AnswerList.objects.count(), 0)

    def test_add_answer_nonexistent_product(self):
        data = {
            "product_title": "Nonexistent Product",
            "answers": ["A1", "A2"]
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(AnswerList.objects.count(), 0)

    def test_add_answer_server_error(self):
        data = {
            "product_title": "Sample Product 2",
            "answers": ["A1", "A2"]
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(AnswerList.objects.count(), 0)