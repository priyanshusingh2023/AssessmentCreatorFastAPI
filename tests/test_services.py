import unittest
from unittest.mock import patch
from main.services import generate_assessment

class TestGenerateAssessment(unittest.TestCase):

    @patch('main.services.get_result')
    @patch('main.services.generate_prompt_assessment')
    def test_generate_assessment_valid(self, mock_generate_prompt, mock_get_result):
        mock_generate_prompt.return_value = "Generated prompt"
        mock_get_result.return_value = "Generated result"

        assessment_data = {
            "role": "Developer",
            "cards": [
                {
                    "keywords": ["Python", "Flask"],
                    "tools": ["PyCharm", "Postman"],
                    "level": "Intermediate",
                    "noOfQuestions": 10
                }
            ]
        }
        result = generate_assessment(assessment_data)
        self.assertIn("Generated result", result)

    def test_generate_assessment_invalid_data_type(self):
        with self.assertRaises(ValueError):
            generate_assessment("invalid data type")

    def test_generate_assessment_empty_data(self):
        with self.assertRaises(ValueError):
            generate_assessment({})

    def test_generate_assessment_missing_role_or_cards(self):
        with self.assertRaises(ValueError):
            generate_assessment({"role": "Developer"})
        with self.assertRaises(ValueError):
            generate_assessment({"cards": []})

    def test_generate_assessment_missing_card_fields(self):
        assessment_data = {
            "role": "Developer",
            "cards": [
                {
                    "keywords": ["Python", "Flask"],
                    # Missing 'tools', 'level', and 'noOfQuestions'
                }
            ]
        }
        with self.assertRaises(ValueError):
            generate_assessment(assessment_data)

if __name__ == "__main__":
    unittest.main()
