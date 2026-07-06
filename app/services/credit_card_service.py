from app.extensions import db
from app.models.credit_card import CreditCard
from app.schemas.credit_card_schema import CreditCardCreateSchema, CreditCardUpdateSchema

class CreditCardService:
    def get_all_by_user(self, user_id: int) -> list[CreditCard]:
        return CreditCard.query.filter_by(user_id=user_id, is_active=True).all()

    def get_by_id_and_user(self, card_id: int, user_id: int) -> CreditCard:
        card = CreditCard.query.filter_by(id=card_id, is_active=True).first()
        
        if not card:
            raise LookupError("Tarjeta de credito no encontrada")
            
        if card.user_id != user_id:
            raise PermissionError("No tienes permisos para acceder a esta tarjeta")
            
        return card

    def create(self, data: CreditCardCreateSchema, user_id: int) -> CreditCard:
        credit_card = CreditCard(
            user_id=user_id,
            card_name=data.card_name,
            credit_limit=data.credit_limit,
            closing_day=data.closing_day,
            due_day=data.due_day,
            debt_amount=0.00
        )
        db.session.add(credit_card)
        db.session.commit()
        return credit_card

    def update(self, card_id: int, data: CreditCardUpdateSchema, user_id: int) -> CreditCard:
        card = self.get_by_id_and_user(card_id, user_id)

        if data.card_name is not None:
            card.card_name = data.card_name
        if data.credit_limit is not None:
            card.credit_limit = data.credit_limit
        if data.debt_amount is not None:
            card.debt_amount = data.debt_amount

        db.session.commit()
        return card

    def delete(self, card_id: int, user_id: int) -> None:
        card = self.get_by_id_and_user(card_id, user_id)
        card.is_active = False
        db.session.commit()

card_service = CreditCardService()
