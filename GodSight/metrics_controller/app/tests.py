from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Blockchain, ChainMetric  # Import your models accordingly


class APITests(APITestCase):

    def test_create_metric(self):
        """
        Ensure we can create a new metric object.
        """
        url = reverse('create-metric')  # Update 'create-metric' to match your URL name
        data = {
            'metric_name': 'NewMetric',
            'blockchain': 'Avalanche',
            'sub_chain': 'c',
            'display_name': 'New Metric Display Name',
            'description': 'A new metric for testing',
            'category': 'General',
            'type': 'Format 1',
            'formula': {}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChainMetric.objects.count(), 1)
        self.assertEqual(ChainMetric.objects.get().metric_name, 'NewMetric')

    def test_get_selection_data(self):
        """
        Ensure we can retrieve selection data.
        """
        url = reverse('get-selection-data')  # Update 'get-selection-data' to match your URL name
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Further assertions can be made based on the expected structure of your response data

    def test_swagger_ui(self):
        """
        Ensure the Swagger UI page loads.
        """
        url = reverse('schema-swagger-ui')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redoc_ui(self):
        """
        Ensure the ReDoc UI page loads.
        """
        url = reverse('schema-redoc')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
