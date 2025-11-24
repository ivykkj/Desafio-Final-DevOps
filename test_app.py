import unittest
from app import app
import werkzeug

# Patch temporário para adicionar o atributo '__version__' em werkzeug 
if not hasattr(werkzeug, '__version__'): 
    werkzeug.__version__ = "mock-version"

class APITestCase(unittest.TestCase): 
    @classmethod 
    def setUpClass(cls): 
        # Criação do cliente de teste 
        cls.client = app.test_client()
    
    def test_get_items_endpoint(self):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        expected_data = {"items": ["item1", "item2", "item3"]}
        self.assertEqual(response.json, expected_data)

    def test_protected_with_token(self):
        login_response = self.client.get('/login')
        token = login_response.json['access_token']
        response = self.client.post(
            '/protected',
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Protected route"})

    def test_swagger_ui_loads(self):
        response = self.client.get('/swagger')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Swagger UI', response.data)

if __name__ == '__main__':
    unittest.main()

