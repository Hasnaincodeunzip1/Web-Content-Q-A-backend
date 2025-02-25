from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch, MagicMock

#  We're providing a basic example test case here.  For a real project,
#  you would write more comprehensive tests to cover different scenarios.

class AnswerViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('answer')  # 'answer' is the name we gave our URL pattern

    @patch('qa.views.model.generate_content') # Mocking the gemini api call
    def test_successful_response(self, mock_generate_content):
        # Mock the Gemini API response
        mock_response = MagicMock()
        mock_response.text = "This is a test answer."
        mock_generate_content.return_value = mock_response

        data = {
            'urls': ['https://www.example.com'],
            'question': 'What is the purpose of this website?',
        }
        #Mocking the request
        with patch('qa.views.requests.get') as mock_get:
          mock_get.return_value.status_code = 200
          mock_get.return_value.text = "<p>This is example website content.</p>"

          response = self.client.post(self.url, data, format='json')
          self.assertEqual(response.status_code, status.HTTP_200_OK)
          self.assertEqual(response.data, {'answer': 'This is a test answer.'})

    def test_invalid_url(self):
        data = {
            'urls': ['invalid-url'],  # Invalid URL format
            'question': 'A question',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # You could also check the specific error message in response.data

    @patch('qa.views.requests.get')
    def test_url_fetch_error(self, mock_get):
      # Simulate a network error during URL fetching
      mock_get.side_effect = requests.RequestException("Network error")

      data = {
          'urls': ['https://www.example.com'],
          'question': 'What is the purpose of this website?',
      }
      response = self.client.post(self.url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      self.assertIn("Error fetching URL", response.data['error'])

    @patch('qa.views.model.generate_content')
    def test_gemini_api_error(self, mock_generate_content):
        # Simulate an error from the Gemini API
        mock_generate_content.side_effect = Exception("Gemini API error")
        data = {
          'urls': ['https://www.example.com'],
          'question': 'What is the purpose of this website?',
        }
        #Mocking the request
        with patch('qa.views.requests.get') as mock_get:
          mock_get.return_value.status_code = 200
          mock_get.return_value.text = "<p>This is example website content.</p>"
          response = self.client.post(self.url, data, format='json')
          self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
          self.assertIn("Gemini API error", response.data['error'])