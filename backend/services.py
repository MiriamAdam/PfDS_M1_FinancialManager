from backend.controller import TransactionsController
from backend.controller.budgets_controller import BudgetsController
from backend.controller.reports_controller import ReportsController
from backend.utils import DbCreator

budgets_service = BudgetsController()
transactions_service = TransactionsController(budgets_service)
reports_service = ReportsController(budgets_service, transactions_service)

db_creator = DbCreator()