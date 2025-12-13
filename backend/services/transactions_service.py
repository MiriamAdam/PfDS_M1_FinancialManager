from backend.db import SqliteDb
from backend.model import Transaction, Category


class TransactionsService:
    """Service for adding and retrieving transactions from the database."""
    def __init__(self, budgets_service):
        self.storage = SqliteDb()
        self.budgets = budgets_service.budgets


    def add_transaction(self, data):
        """
        Adds a transaction to the database if transaction doesn't exceed a set budget limit.

        :param data: transaction data
        """
        amount = float(data['amount'])
        category_name = data['category_name']
        sub_category = data['sub_category']

        category = Category.from_category_as_string(category_name)
        budget = self.budgets.get(category)

        if not category.is_income and budget:
            current_spent = self.budgets.get_current_spent_amount(category_name, budget)
            budget.spent = current_spent
            if budget.get_remaining() - amount < 0:
                    raise ValueError(f"Budget for category {category_name} is exceeded.")

        transaction = Transaction(amount, category_name, sub_category)
        self.storage.save_transaction(transaction)

        if budget:
            budget.add_expense(amount)


    def get_transactions(self, category_name=None):
        """
        Returns a dictionary of transaction objects of the database, optionally filtered by category.

        :param category_name: category of the transactions, optional
        :return: a list of transactions in the database
        """
        if category_name:
            transactions = self.storage.load_transactions_by_category(category_name)
        else:
            transactions = self.storage.load_all_transactions()

        return [t.to_dict() for t in transactions]

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
            transactions = self.storage.load_transactions_by_exact_date(exact_date)
        elif start_date and end_date:
            transactions = self.storage.load_transactions_by_date_range(start_date, end_date)
        elif start_date:
            transactions = self.storage.load_transactions_by_from_date(start_date)
        elif end_date:
            transactions = self.storage.load_transactions_by_until_date(end_date)
        else:
            transactions = self.storage.load_all_transactions()

        return [t.to_dict() for t in transactions]

    def get_transactions_by_sub_category(self, sub_category):
        """
        Gets all transactions matching a given sub_category.

        :param sub_category: sub_category of the transactions
        :return: a list of transactions of the given sub_category
        """
        transactions = self.storage.load_transactions_by_sub_category(sub_category)

        return [t.to_dict() for t in transactions]

    def get_all_categories(self):
        return [
            {
                "category_name": cat.category_name,
                "sub_categories": cat.sub_categories,
                "is_income": cat.is_income
            }
            for cat in Category
        ]
