import unittest
import json
from main.app import app
class AssessmentCreatorTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('api/v2/Assessment_creator/')
        self.assertEqual(response.status_code, 200)

    def test_create_assessment_valid_request(self):
        request_data = {
            "role": "Developer",
            "cards": [
                {
                    "keywords": ["Python", "Flask"],
                    "tools": ["PyCharm", "Postman"],
                    "level": "low",
                    "noOfQuestions": 10
                }
            ]
        }
        response = self.app.post('api/v2/Assessment_creator/generate_assessment', json=request_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn('assessment', data)

    def test_create_assessment_missing_fields(self):
        request_data = {
            "role": "Developer",
            "cards": [
                {
                    "keywords": ["Python", "Flask"],
                    "level": "Intermediate"
                    # Missing 'tools' and 'noOfQuestions'
                }
            ]
        }
        response = self.app.post('api/v2/Assessment_creator/generate_assessment', json=request_data)
        self.assertEqual(response.status_code, 500)  

    def test_create_assessment_invalid_level(self):
        request_data = {
            "role": "Developer",
            "cards": [
                {
                    "keywords": ["Python", "Flask"],
                    "tools": ["PyCharm", "Postman"],
                    "level": "InvalidLevel",
                    "noOfQuestions": 10
                }
            ]
        }
        response = self.app.post('api/v2/Assessment_creator/generate_assessment', json=request_data)
        self.assertEqual(response.status_code, 500)  # Assuming the API returns 400 for invalid level

if __name__ == "__main__":
    unittest.main()
