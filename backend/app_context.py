from backend.services import TransactionsService
from backend.services.budgets_service import BudgetsService
from backend.services.reports_service import ReportsService

budgets_service = BudgetsService()
transactions_service = TransactionsService(budgets_service)
reports_service = ReportsService(budgets_service, transactions_service)