from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing_extensions import Self
import re

class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @field_validator('first_name', 'last_name')
    def names_not_empty(cls, value:str) -> str:
        if not value.strip():
            raise ValueError("Este campo no puede estar vacio")
        return value.strip()
    
    @field_validator('password')
    def check_password_strength(cls, value: str) -> str:
        if not any(char.isupper() for char in value):
            raise ValueError("La contraseña debe incluir al menos una letra mayuscula")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_+-]', value):
            raise ValueError("La contraseña debe incluir al menos un caracter especial")        
        if not any(char.isdigit() for char in value):
            raise ValueError("La contraseña debe incluir al menos un numero")
        return value
    
    @model_validator(mode='after')
    def verify_password_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Las contraseñas debe coincidir")
        return self

class LoginSchema(BaseModel):
    email: EmailStr
    password: str