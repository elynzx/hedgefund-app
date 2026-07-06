from db import db
from app.models.transaction import Transaction, TransactionType
from app.models.bank_account import BankAccount
from app.models.credit_card import CreditCard
from app.schemas.transaction_schema import TransactionCreateSchema

class TransactionService:
    def __init__(self):
        self._transaction_handlers = {
            TransactionType.INCOME: self._process_income,
            TransactionType.EXPENSE: self._process_expense,
            TransactionType.TRANSFER: self._process_transfer,
            TransactionType.CREDIT_CARD_PAYMENT: self._process_cc_payment
        }

    def get_all_by_user(self, user_id: int) -> list[Transaction]:
        return Transaction.query.filter_by(user_id=user_id)\
                                .order_by(Transaction.date.desc(), Transaction.created_at.desc())\
                                .all()

    def create(self, data: TransactionCreateSchema, user_id: int) -> Transaction:
        
        transaction = Transaction(
            user_id=user_id,
            category_id=data.category_id,
            transaction_type=data.transaction_type.value,
            amount=data.amount,
            description=data.description,
            source_account_id=data.source_account_id,
            source_card_id=data.source_card_id,
            destination_account_id=data.destination_account_id,
            destination_card_id=data.destination_card_id
        )
        if data.date:
            transaction.date = data.date

        handler = self._transaction_handlers.get(data.transaction_type)
        if not handler:
            raise ValueError("Tipo de transaccion incorrecta")
        
        handler(data, user_id)

        db.session.add(transaction)
        db.session.commit()
        return transaction

    def _process_income(self, data: TransactionCreateSchema, user_id: int) -> None:
        if not data.destination_account_id:
            raise ValueError("Se requiere una cuenta bancaria de destino para registrar un ingreso")
        
        account = BankAccount.query.filter_by(id=data.destination_account_id, user_id=user_id, is_active=True).first()
        if not account:
            raise LookupError("Cuenta de destino no encontrada")
            
        account.current_balance = float(account.current_balance) + data.amount

    def _process_expense(self, data: TransactionCreateSchema, user_id: int) -> None:
        if not data.source_account_id and not data.source_card_id:
            raise ValueError("Se requiere una cuenta bancaria de origen o una tarjeta para registrar un gasto")
        
        if data.source_account_id:
            account = BankAccount.query.filter_by(id=data.source_account_id, user_id=user_id, is_active=True).first()
            if not account:
                raise LookupError("Cuenta bancnaria de origen no encontrada")
            if float(account.current_balance) < data.amount:
                raise ValueError("Saldo insuficiente en la cuenta bancaria.")
            account.current_balance = float(account.current_balance) - data.amount
        
        elif data.source_card_id:
            card = CreditCard.query.filter_by(id=data.source_card_id, user_id=user_id, is_active=True).first()
            if not card:
                raise LookupError("Tarjeta de credito no encontrada")
            
            available_credit = float(card.credit_limit) - float(card.debt_amount)
            if available_credit < data.amount:
                raise ValueError("Linea de credito insuficiente en la tarjeta")
            card.debt_amount = float(card.debt_amount) + data.amount

    def _process_transfer(self, data: TransactionCreateSchema, user_id: int) -> None:
        if not data.source_account_id or not data.destination_account_id:
            raise ValueError("Se requieren las cuentas de origen y destino para una transferencia")
        
        source_account = BankAccount.query.filter_by(id=data.source_account_id, user_id=user_id, is_active=True).first()
        destination_account = BankAccount.query.filter_by(id=data.destination_account_id, user_id=user_id, is_active=True).first()
        
        if not source_account or not destination_account:
            raise LookupError("Una o ambas cuentas bancarias no fueron encontradas")
        if float(source_account.current_balance) < data.amount:
            raise ValueError("Saldo insuficiente para realizar la transferencia")
            
        source_account.current_balance = float(source_account.current_balance) - data.amount
        destination_account.current_balance = float(destination_account.current_balance) + data.amount

    def _process_cc_payment(self, data: TransactionCreateSchema, user_id: int) -> None:
        if not data.source_account_id or not data.destination_card_id:
            raise ValueError("Se requiere la cuenta bancaria de origen y la tarjeta de destino")
            
        account = BankAccount.query.filter_by(id=data.source_account_id, user_id=user_id, is_active=True).first()
        card = CreditCard.query.filter_by(id=data.destination_card_id, user_id=user_id, is_active=True).first()
        
        if not account or not card:
            raise LookupError("La cuenta bancaria o la tarjeta no fueron encontradas")
        if float(account.current_balance) < data.amount:
            raise ValueError("Saldo insuficiente en la cuenta bancaria para pagar la tarjeta")
            
        account.current_balance = float(account.current_balance) - data.amount
        card.debt_amount = max(0.00, float(card.debt_amount) - data.amount)

transaction_service = TransactionService()
