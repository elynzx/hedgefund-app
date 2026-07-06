from app.extensions import bcrypt
import os
from cryptography.fernet import Fernet
import base64

def hash_password(input_password: str) -> str:
    hashed_password = bcrypt.generate_password_hash(input_password).decode('utf-8')
    return hashed_password

def verify_password(hashed_password:str, input_password:str ) -> bool:
    is_valid= bcrypt.check_password_hash(hashed_password, input_password)
    return is_valid

class CryptoHelper():
    def __init__(self):
        self._key = os.getenv('FERNET_KEY')
        self._validate_key()
        self.fernet = Fernet(self._key)
        
    def encrypt(self, value: str | int | float | bool ) -> str:
        bytes_value = str(value).encode('utf-8')
        encrypted_value = self.fernet.encrypt(bytes_value)
        return encrypted_value.decode('utf-8')
    
    def decrypt(self, value: str) -> str:
        bytes_value=value.encode('utf-8')
        decrypted_value = self.fernet.decrypt(bytes_value)
        return decrypted_value.decode('utf-8')
    
    def  _validate_key(self):
        if not self._key:
            raise ValueError('FERNET_KEY is not set')
        try:
            bytes_key= base64.urlsafe_b64decode(self._key)
            if len(bytes_key) != 32:
                raise ValueError('Invalid Key length')
        except  ValueError as e:
            raise ValueError(f'{e}')