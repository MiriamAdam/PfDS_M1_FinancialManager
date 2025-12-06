from datetime import datetime

from backend.model import Transaction, Category, SqliteDb, Budget

class TransactionsController:
    """Controller for adding and retrieving transactions from the database."""
    def __init__(self, budgets_service):
        self.storage = SqliteDb()
        self.budgets = budgets_service.budgets


    def add_transaction(self, amount: float, category_name: str, sub_category: str):
        """
        Adds a transaction to the database.
        Updates the budget for the category if set.
        Raises ValueError if the expenditure would exceed the budget.

        :param category_name: the category of the transaction
        :param sub_category: sub_category of the transaction
        :param amount: the transaction amount
        """
        category = Category.from_category_as_string(category_name)
        last_transaction = self.storage.load_all_transactions().first()
        this_year = datetime.now().year
        this_month = datetime.now().month
        # if it's a new month budget is reseted
        if category in self.budgets and (last_transaction.date.year != this_year or last_transaction.date.month != this_month):
            self.budgets[category].reset_budget()
        if category not in self.budgets or self.budgets[category].get_remaining() - amount >= 0:
            transaction = Transaction(round(amount, 2), category_name, sub_category)
            self.storage.save_transaction(transaction)
            if category in self.budgets:
                self.budgets[category].add_expense(amount)
        else:
            raise ValueError(f"Budget for category {category_name} is exceeded.")

    def get_all_transactions(self):
        """
        Returns all transactions in the database.

        :return: a list of all transactions in the database
        """
        return self.storage.load_all_transactions()

    def get_transactions_by_date(self, exact_date=None, start_date=None, end_date=None):
        """
        Get transactions based on optional date filters.
        If no parameters are provided, all transactions are returned.
        - exact_date: returns transactions for that specific date
        - start_date: returns transactions from that day onward
        - end_date: returns transactions up to that day
        - start_date and end_date: returns transactions within the date range

        :param exact_date: (optional) exact date of the transaction
        :param start_date: (optional) start date of a timespan
        :param end_date: (optional) end date of a timespan
        :return: a list of transactions matching the date filters
        """
        if exact_date:
            return self.storage.load_transactions_by_exact_date(exact_date)
        elif start_date and end_date:
            return self.storage.load_transactions_by_date_range(start_date, end_date)
        elif start_date:
            return self.storage.load_transactions_by_from_date(start_date)
        elif end_date:
            return self.storage.load_transactions_by_until_date(end_date)
        else:
            return self.storage.load_all_transactions()

    def get_transactions_by_category(self, category_name):
        """
        Returns all transactions for a given category.

        :param category_name: category of the transactions
        :return: list of transactions in the specified category
        """
        return self.storage.load_transactions_by_category(category_name)

    def get_transactions_by_sub_category(self, sub_category):
        """
        Gets all transactions matching a given sub_category.

        :param sub_category: sub_category of the transactions
        :return: a list of transactions of the given sub_category
        """
        return self.storage.load_transactions_by_sub_category(sub_category)

