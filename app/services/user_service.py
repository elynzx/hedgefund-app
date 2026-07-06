from app.models.user import User
from app.schemas.user_schema import UserUpdateSchema
from db import db

class UserService:
    def get_by_id(self, user_id: int) -> User | None:
        return User.query.get(user_id)

    def update_profile(self, user_id: int, data: UserUpdateSchema) -> User:
        user = self.get_by_id(user_id)
        if not user:
            raise KeyError("Usuario no encontrado.")

        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name
        if data.currency is not None:
            user.currency = data.currency
        if data.monthly_income is not None:
            user.monthly_income = data.monthly_income

        db.session.commit()
        return user

user_service = UserService()