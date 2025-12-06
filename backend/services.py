from backend.controller import TransactionsController
from backend.controller.budgets_controller import BudgetsController

budgets_service = BudgetsController()
transactions_service = TransactionsController(budgets_service)