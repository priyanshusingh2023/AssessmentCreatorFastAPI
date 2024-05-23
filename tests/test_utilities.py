import unittest
from unittest.mock import patch, Mock
import requests
from main.utilities import generate_prompt_assessment,get_result
class TestUtilities(unittest.TestCase):

    def test_generate_prompt_assessment_valid(self):
        assessment_data = {
            "role": "Developer",
            "card": {
                "keywords": ["Python", "Flask"],
                "tools": ["PyCharm", "Postman"],
                "level": "medium",
                "noOfQuestions": 10
            }
        }
        result = generate_prompt_assessment(assessment_data)
        expected_prompt = "I want 10 assessment questions of medium complexity for Developer on Python, Flask using PyCharm, Postman."
        self.assertEqual(result, expected_prompt)

    def test_generate_prompt_assessment_missing_fields(self):
        assessment_data = {
            "role": "Developer",
            "card": {
                "keywords": ["Python", "Flask"]
                # Missing 'tools', 'level', and 'noOfQuestions'
            }
        }
        with self.assertRaises(ValueError):
            generate_prompt_assessment(assessment_data)

    def test_generate_prompt_assessment_invalid_level(self):
        assessment_data = {
            "role": "Developer",
            "card": {
                "keywords": ["Python", "Flask"],
                "tools": ["PyCharm", "Postman"],
                "level": "invalid",
                "noOfQuestions": 10
            }
        }
        with self.assertRaises(ValueError):
            generate_prompt_assessment(assessment_data)

    @patch('main.utilities.requests.post')
    def test_get_result_valid(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "Generated content"
                            }
                        ]
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        prompt = "Test prompt"
        result = get_result(prompt)
        self.assertEqual(result, "Generated content")

    @patch('main.utilities.requests.post')
    def test_get_result_request_exception(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Error")
        prompt = "Test prompt"
        with self.assertRaises(Exception) as context:
            get_result(prompt)
        self.assertIn("Error in getting response from Gemini API", str(context.exception))

if __name__ == "__main__":
    unittest.main()
