from app import bcrypt

def hash_password(input_password: str) -> str:
    hashed_password = bcrypt.generate_password_hash(input_password).decode('utf-8')
    return hashed_password

def verify_password(hashed_password:str, input_password:str ) -> bool:
    is_valid= bcrypt.check_password_hash(hashed_password, input_password)
    return is_valid