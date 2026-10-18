import hashlib
import secrets

class AuthService:
    def __init__(self):
        # In a real app, this would connect to PostgreSQL or MySQL
        self.users_db = {}

    def hash_password(self, password: str, salt: str) -> str:
        """Hashes the password using SHA-256 and a salt."""
        return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

    def generate_verification_token(self) -> str:
        """Generates a secure, cryptographic 24-hour HMAC token (mock)."""
        return secrets.token_urlsafe(32)

    def register_user(self, email: str, password: str):
        """
        QM-5: Implement user registration endpoint and password hashing.
        """
        if email in self.users_db:
            return {"status": 409, "message": "An account with this email already exists"}
        
        salt = secrets.token_hex(16)
        hashed_pw = self.hash_password(password, salt)
        verification_token = self.generate_verification_token()

        # Save to DB
        self.users_db[email] = {
            "email": email,
            "salt": salt,
            "password_hash": hashed_pw,
            "status": "pending_verification",
            "verification_token": verification_token
        }

        # Mocking the SendGrid SMTP Relay dispatch
        print(f"[EMAIL SENT] To: {email} | Verification Token: {verification_token}")

        return {"status": 201, "message": "Registration successful. Please verify your email."}

# Example usage for testing
if __name__ == "__main__":
    auth = AuthService()
    print(auth.register_user("alice@example.com", "SuperSecretPassword123"))