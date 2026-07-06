from db import db
from app.models.bank_account import BankAccount
from app.schemas.bank_account_schema import BankAccountCreateSchema, BankAccountUpdateSchema

class BankAccountService:
    def get_all_by_user(self, user_id: int) -> list[BankAccount]:
        return BankAccount.query.filter_by(user_id=user_id, is_active=True).all()

    def get_by_id_and_user(self, account_id: int, user_id: int) -> BankAccount:
        account = BankAccount.query.filter_by(id=account_id, is_active=True).first()

        if not account:
            raise LookupError("Cuenta bancaria no encontrada")

        if account.user_id != user_id:
            raise PermissionError("No tienes permisos para acceder a esta cuenta bancaria")
            
        return account

    def create(self, data:BankAccountCreateSchema, user_id: int) -> BankAccount:
        bank_account = BankAccount(
            user_id=user_id,
            account_name=data.account_name,
            account_type=data.account_type.value,
            current_balance=data.current_balance
        )
        db.session.add(bank_account)
        db.session.commit()
        return bank_account

    def update(self, account_id: int, data:BankAccountUpdateSchema , user_id: int) -> BankAccount:
        account = self.get_by_id_and_user(account_id, user_id)

        if data.account_name is not None:
            account.account_name = data.account_name
        if data.account_type is not None:
            account.account_type = data.account_type.value
        if data.current_balance is not None:
            account.current_balance = data.current_balance

        db.session.commit()
        return account

    def delete(self, account_id: int, user_id: int) -> None:
        account = self.get_by_id_and_user(account_id, user_id)
        account.is_active = False
        db.session.commit()

bank_account_service = BankAccountService()
