from backend.controller import TransactionsController
from backend.controller.budgets_controller import BudgetsController
from backend.utils import DbCreator

budgets_service = BudgetsController()
transactions_service = TransactionsController(budgets_service)
db_creator = DbCreator()
