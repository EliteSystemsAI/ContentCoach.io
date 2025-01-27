import unittest
from unittest.mock import patch, MagicMock
from app.chat_handler import generate_content
from app.models import User

class TestChatHandler(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.test_user = User(
            name="Test User",
            business_niche="Digital Marketing",
            content_goals="grow social media presence"
        )
        self.test_message = "How can I improve my content strategy?"

    @patch('app.chat_handler.client')
    def test_successful_content_generation(self, mock_client):
        """Test successful content generation"""
        # Mock the OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Here's your content strategy advice..."))
        ]
        mock_client.chat.completions.create.return_value = mock_response

        # Call the function
        response = generate_content(self.test_user, self.test_message)

        # Verify the response
        self.assertEqual(response, "Here's your content strategy advice...")

        # Verify the OpenAI API was called with correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        
        self.assertEqual(call_args['model'], "gpt-3.5-turbo")
        self.assertEqual(len(call_args['messages']), 2)
        self.assertEqual(call_args['messages'][0]['role'], "system")
        self.assertEqual(call_args['messages'][1]['role'], "user")
        self.assertEqual(call_args['messages'][1]['content'], self.test_message)

    @patch('app.chat_handler.client')
    def test_empty_response_handling(self, mock_client):
        """Test handling of empty response from OpenAI"""
        # Mock an empty response
        mock_response = MagicMock()
        mock_response.choices = []
        mock_client.chat.completions.create.return_value = mock_response

        # Call the function
        response = generate_content(self.test_user, self.test_message)

        # Verify error handling
        self.assertTrue(response.startswith("An error occurred:"))
        self.assertIn("No response choices returned from OpenAI", response)

    @patch('app.chat_handler.client')
    def test_api_error_handling(self, mock_client):
        """Test handling of API errors"""
        # Mock an API error
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        # Call the function
        response = generate_content(self.test_user, self.test_message)

        # Verify error handling
        self.assertTrue(response.startswith("An error occurred:"))
        self.assertIn("API Error", response)

if __name__ == '__main__':
    unittest.main()
