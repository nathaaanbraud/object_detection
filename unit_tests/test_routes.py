import unittest
from flask.testing import FlaskClient
from src.app import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up the test case.

        This method initializes the Flask test client before each test.
        """
        self.app: FlaskClient = create_app().test_client()

    def test_index(self) -> None:
        """
        Test the index route.

        This test verifies that the index route ('/') returns a status code of 200.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()