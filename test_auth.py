import unittest
from auth_service import AuthService

class TestAuthenticationWorkflow(unittest.TestCase):
    
    def setUp(self):
        """Set up a fresh instance of the AuthService before each test."""
        self.auth = AuthService()

    def test_successful_registration(self):
        """Test that a new user is registered successfully with HTTP 201."""
        response = self.auth.register_user("alice@example.com", "SuperSecretPassword123")
        
        # Check HTTP status code
        self.assertEqual(response["status"], 201)
        # Check success message
        self.assertEqual(response["message"], "Registration successful. Please verify your email.")
        # Ensure user is in the mock database
        self.assertIn("alice@example.com", self.auth.users_db)
        # Ensure the status is pending verification
        self.assertEqual(self.auth.users_db["alice@example.com"]["status"], "pending_verification")

    def test_duplicate_registration(self):
        """Test that registering the same email twice returns HTTP 409 Conflict."""
        # Register the user first
        self.auth.register_user("bob@example.com", "AnotherPassword123")
        
        # Try registering the exact same email again
        response = self.auth.register_user("bob@example.com", "NewPassword456")
        
        # Check HTTP status code for conflict
        self.assertEqual(response["status"], 409)
        self.assertEqual(response["message"], "An account with this email already exists")

    def test_password_hashing_logic(self):
        """Test that the password is hashed and not stored in plain text."""
        password = "MySecurePassword"
        salt = "random_salt_123"
        
        hashed = self.auth.hash_password(password, salt)
        
        # Ensure the hash is not equal to the plain text password
        self.assertNotEqual(hashed, password)
        # Ensure SHA-256 produces a 64-character hex string
        self.assertEqual(len(hashed), 64)

if __name__ == '__main__':
    unittest.main()