from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Product, QuestionList
from api.views import get_questions_list_for_product
from django.http import JsonResponse
import json

class QuestionListTestCase(TestCase):
    def setUp(self):

        self.product = Product.objects.create(
            title="Sample Product",
            attributes={"color": "red", "size": "medium"}
        )

        self.product2 = Product.objects.create(
            title="Sample Product 2",
            attributes={"color": "blue", "size": "large"}
        )

        self.question_list = QuestionList.objects.create(
            product=self.product,
            question_list=[
                ["question1", "question2"]
            ]
        )

    def test_get_questions_list_for_product(self):
        url = reverse('get_questions_list_for_product', args=[self.product.title])
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response), JsonResponse)

        response_dict = json.loads(response.content)
        
        self.assertEqual(response_dict, {"questions": [["question1", "question2"]]})

    def test_get_questions_list_for_nonexistent_product(self):
        url = reverse('get_questions_list_for_product', args=['Nonexistent Product'])
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_questions_list_with_missing_questions_list(self):
        url = reverse('get_questions_list_for_product', args=['Sample Product 2'])  # Use an empty string as a placeholder
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)