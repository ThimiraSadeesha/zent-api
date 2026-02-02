from cryptography.fernet import Fernet
import os
import base64
from dotenv import load_dotenv
load_dotenv()

# //add comment
class EncryptionService:
    def __init__(self):
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            raise ValueError("ENCRYPTION_KEY environment variable not set")
        self.cipher = Fernet(key.encode())

    def encrypt(self, data: str) -> str:
        if not data:
            return ""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt(self, encrypted_data: str) -> str:
        if not encrypted_data:
            return ""
        decoded = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(decoded)
        return decrypted.decode()


encryption_service = EncryptionService()
