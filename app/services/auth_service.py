from app.models.user import User
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from app.utils.security import hash_password, verify_password, CryptoHelper
from db import db
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthService:
    def find_by_email(self, email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    def register(self, data: RegisterSchema) -> User:
        
        if self.find_by_email(data.email) is not None:
            raise ValueError('El correo ya está registrado')
        
        hashed_password = hash_password(data.password)
        
        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        return user

    def login(self, data:LoginSchema) -> dict:
        user = self.find_by_email(data.email)
        
        if user is None:
            raise PermissionError('Usuario no encontrado')
        
        if not verify_password(user.password_hash ,data.password):
            raise PermissionError('Contraseña incorrecta')

        if not user.is_active:
            raise ValueError('La cuenta esta desactivada')            

        crypto = CryptoHelper()
        hashed_id = crypto.encrypt(user.id)
        
        access_token = create_access_token(
            identity=hashed_id,
            additional_claims={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        )
        
        refresh_token = create_refresh_token(
            identity=hashed_id
        )
        
        return{
            'access': access_token,
            'refresh': refresh_token,
            'user': user
        }
        
auth_service = AuthService()