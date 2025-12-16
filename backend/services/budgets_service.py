from datetime import datetime

from backend.db import SqliteDb
from backend.model import Category, Budget


class BudgetsService:
    """Service for setting, updating and deleting budgets from the database."""
    def __init__(self):
        self.storage = SqliteDb()
        self.budgets: dict[Category, Budget] = {}
        self._load_budgets_from_storage()

    def _load_budgets_from_storage(self):
        """Loads persistent budget limits from the database and ensures spent amounts of budgets are current."""
        for category_name, limit in self.storage.load_all_budgets().items():
            category = Category.from_category_as_string(category_name)
            if category:
                self.budgets[category] = Budget(category, limit)
        self.ensure_budgets_are_current()

    def get_all_budgets(self):
        """Returns a dictionary of all budgets in the database."""
        result = []

        for category, budget in self.budgets.items():
            category_name = category.category_name
            current_spent_amount = self.get_current_spent_amount(category_name)

            budget.spent = current_spent_amount

            result.append({
                'category_name': category_name,
                'limit': budget.limit,
                'spent': current_spent_amount,
                'remaining': budget.get_remaining()
            })

        return result

    def get_all_budget_objects(self):
        """Returns all budgets in the database as budget objects."""
        return self.budgets.items()

    def ensure_budgets_are_current(self):
        """Checks if a new month has begun and then resets spent amount of budgets."""
        current_month = datetime.now().strftime("%Y-%m")
        for category, budget in self.budgets.items():
            last_reset = self.storage.get_budget_reset_month(category.category_name)
            if last_reset != current_month:
                budget.reset_spent()
                self.storage.update_budget_reset_month(category.category_name, current_month)
                self.storage.save_budget(category.category_name, budget.limit)

    def get_current_spent_amount(self, category: str):
        """
        Sums up all amounts already spent for a budget category in the current month.

        :param category: the category of the budget
        """
        first_of_month = datetime(datetime.now().year, datetime.now().month, 1)
        transactions = self.storage.load_transactions_by_category(category, start_date=first_of_month)
        sum_spent = 0
        for t in transactions:
            category = Category.from_category_as_string(t.category_name)
            if not category.is_income:
                sum_spent += t.amount
        return sum_spent


    def set_budget(self, data):
        """
        Sets the budget for a category with the given limit.

        :param data: the budget data
        """
        category_name = data['category_name']
        limit = float(data['limit'])

        category = Category.from_category_as_string(category_name)
        first_day_of_month = datetime(datetime.now().year, datetime.now().month, 1)
        transactions = self.storage.load_transactions_by_category(category_name, start_date=first_day_of_month)
        amount_already_spent = sum(t.amount for t in transactions)
        if amount_already_spent <= limit:
            self.budgets[category] = Budget(category, limit, amount_already_spent)
            self.storage.save_budget(category.category_name, limit)
        else:
            raise ValueError(f"You have already exceeded the budget limit this month.")

    def delete_budget(self, category_string: str):
        """Deletes a budget from self.budgets and database"""
        category = Category.from_category_as_string(category_string)
        if category in self.budgets:
            del self.budgets[category]
            self.storage.delete_budget(category_string)

    def get_budget_for_category(self, category):
        """
            Returns the Budget object for a given Category.

            :param category: the category object
            :return: the Budget object or None
            """
        return self.budgets.get(category)
