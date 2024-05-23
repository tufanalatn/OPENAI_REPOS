# test_app.py
import pytest
from flask import Flask
from flask_testing import TestCase
from app import app  # Import the Flask app

class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_home(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_ask_valid_request(self):
        valid_data = {
            "image_url": "http://example.com/image.jpg",
            "text": "Some text",
            "prompt": "Some prompt"
        }
        response = self.client.post('/ask', json=valid_data)
        self.assert200(response)
        self.assertIn("response", response.json)

    def test_ask_invalid_request(self):
        invalid_data = {
            "image_url": "",
            "text": "Some text",
            "prompt": "Some prompt"
        }
        response = self.client.post('/ask', json=invalid_data)
        self.assert400(response)
        self.assertIn("error", response.json)

    def test_audio(self):
        response = self.client.get('/audio')
        self.assert200(response)
        self.assertEqual(response.content_type, 'audio/mpeg')

if __name__ == '__main__':
    pytest.main()
