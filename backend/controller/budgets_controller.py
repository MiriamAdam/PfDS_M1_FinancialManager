from datetime import datetime

from backend.model import SqliteDb, Category, Budget


class BudgetsController:
    """Controller for setting, updating and deleting budgets from the database."""
    def __init__(self):
        self.storage = SqliteDb()
        self.budgets: dict[Category, Budget] = {}
        self._load_budgets_from_storage()

    def _load_budgets_from_storage(self):
        """Loads all budgets from the database.
        Sums up all amounts already spent for a budget in current month. """
        for category_name, limit in self.storage.load_all_budgets().items():
            category = Category.from_category_as_string(category_name)
            if category:
                transactions = []
                for t in self.storage.load_transactions_by_category(category_name):
                    dt = datetime.strptime(t.date, '%Y-%m-%d %H:%M:%S.%f')
                    if dt.year == datetime.now().year and dt.month == datetime.now().month:
                        transactions.append(t)
                spent = sum(t.amount for t in transactions)
                self.budgets[category] = Budget(category, limit, spent)
                print(transactions)

    def set_budget(self, category_name: str, limit: float):
        """
        Sets the budget for a category with the given limit.

        :param category_name: the category of the budget
        :param limit: the limit of the budget
        """
        try:
            category = Category.from_category_as_string(category_name)
            self.budgets[category] = Budget(category, limit)
            self.storage.save_budget(category.category_name, limit)
        except Exception as e:
            print('ERROR in set_budget', e)
            raise

    def check_if_budget_is_set(self, category_name: str):
        """
        Checks if a budget is set for the given category.
        """
        category = Category.from_category_as_string(category_name)
        return self.budgets[category]

    def set_budget_with_already_incurred_expenses(self, category: Category, limit: float):
        """
        Sets budget and takes previous expenditure into account.

        :param category: the category of the budget
        :param limit: the limit of the budget
        """
        transactions = self.storage.load_transactions_by_category(category)
        total = 0
        for transaction in transactions:
            total += transaction.amount
        self.budgets[category] = Budget(category, limit, total)

    def check_budget(self, category: Category) -> float:
        """
        Checks how much money is left until a set budget is reached.

        :param category: the category of the budget
        :return: the amount of money left until a budget is reached OR ValueError if budget is not set
        """
        if category in self.budgets:
            return self.budgets[category].get_remaining()
        else:
            raise ValueError(f"Budget for category {category.category_name} is not set.")

    def delete_budget(self, category_string: str):
        """Deletes a budget from self.budgets and database"""
        category = Category.from_category_as_string(category_string)
        if category in self.budgets:
            del self.budgets[category]
            self.storage.delete_budget(category_string)

    def reset_budget(self, category: Category):
        """Resets a set budget if a new month has begun."""
        self.budgets[category].reset_spent()