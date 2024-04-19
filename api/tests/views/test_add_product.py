from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Product, QuestionList
from api.views import add_product
from unittest.mock import patch

class AddProductTestCase(TestCase):
    
    def test_add_product_success(self):
        client = APIClient()
        data = {'product_title': 'New Product'}
        response = client.post(reverse('add_product'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Product.objects.filter(title='New Product').exists())

    def test_add_existing_product(self):
        Product.objects.create(title='Existing Product')
        client = APIClient()
        data = {'product_title': 'Existing Product'}
        response = client.post(reverse('add_product'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_product_with_missing_product_title(self):
        client = APIClient()
        data = {'product_title': ''}
        response = client.post(reverse('add_product'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("api.views.JsonResponse") 
    def test_add_product_raises_internal_server_error(self, mock_json_response):
        mock_json_response.side_effect = Exception("Simulated error")

        client = APIClient()
        data = {'product_title': 'New Product'}
        response = client.post(reverse('add_product'), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)