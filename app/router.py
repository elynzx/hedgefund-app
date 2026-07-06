from flask_restful import Api
from app.resources.auth_resource import *
from app.resources.user_resource import *
from app.resources.category_resource import *
from app.resources.bank_account_resource import *
from app.resources.credit_card_resource import *
from app.resources.transaction_resource import *

api = Api(prefix='/api/v1')

api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LoginResource, '/auth/login')

api.add_resource(UserProfileResource, '/profile')

api.add_resource(CategoryResource, '/categories')

api.add_resource(BankAccountResource, '/accounts')
api.add_resource(ManageBankAccountResource, '/accounts/<int:account_id>')

api.add_resource(CreditCardResource, '/cards')
api.add_resource(ManageCreditCardResource, '/cards/<int:card_id>')

api.add_resource(TransactionResource, '/transactions')
