from backend.controller import TransactionsController
from backend.controller.budgets_controller import BudgetsController
from backend.controller.reports_controller import ReportsController

budgets_service = BudgetsController()
transactions_service = TransactionsController(budgets_service)
reports_service = ReportsController(budgets_service, transactions_service)