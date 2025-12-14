from backend.db import SqliteDb
from backend.model import Transaction, Category


class TransactionsService:
    """Service for adding and retrieving transactions from the database."""
    def __init__(self, budgets_service):
        self.storage = SqliteDb()
        self.budgets_service = budgets_service

    def _signed_amount(self, t):
        """Amounts of transactions are saved absolute. This method adds a minus to negative amounts."""
        category = Category.from_category_as_string(t.category_name)
        return t.amount if category.is_income else -t.amount

    def _convert_if_needed(self, transactions, as_dict):
        """Helper method to convert a list of transactions into a list of dictionaries for api routes."""
        if as_dict:
            result = []
            for t in transactions:
                data = {
                "amount": self._signed_amount(t),
                "category_name": t.category_name,
                "sub_category": t.sub_category,
                "date": str(t.date)
            }
                result.append(data)
            return result
        return transactions

    def add_transaction(self, data):
        """
        Adds a transaction to the database if transaction doesn't exceed a set budget limit.

        :param data: transaction data
        """
        amount = float(data['amount'])
        category_name = data['category_name']
        sub_category = data['sub_category']

        category = Category.from_category_as_string(category_name)
        budget = self.budgets_service.get_budget_for_category(category)

        if not category.is_income and budget:
            current_spent = self.budgets_service.get_current_spent_amount(category_name, budget)
            budget.spent = current_spent
            if budget.get_remaining() - amount < 0:
                    raise ValueError(f"Budget for category {category_name} is exceeded.")

        transaction = Transaction(amount, category_name, sub_category)
        self.storage.save_transaction(transaction)

        if budget:
            budget.add_expense(amount)


    def get_transactions(self, category_name=None, as_dict=False):
        """
        Returns a list of transaction objects of the database, optionally filtered by category.

        :param category_name: (optional) get only transactions of the category
        :param as_dict: (optional) if True, return a dictionary instead of a list of transactions
        :return: a list of transactions in the database
        """
        if category_name:
            transactions = self.storage.load_transactions_by_category(category_name)
        else:
            transactions = self.storage.load_all_transactions()

        return self._convert_if_needed(transactions, as_dict)



    def get_transactions_by_date(self, exact_date=None, start_date=None, end_date=None, as_dict=False):
        """
        Get transactions based on optional date filters.
        If no parameters are provided, all transactions are returned as list of objects.
        - exact_date: returns transactions for that specific date
        - start_date: returns transactions from that day onward
        - end_date: returns transactions up to that day
        - start_date and end_date: returns transactions within the date range

        :param exact_date: (optional) exact date of the transaction
        :param start_date: (optional) start date of a timespan
        :param end_date: (optional) end date of a timespan
        :param as_dict: (optional) if True, return a dictionary instead of a list of transactions
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

        return self._convert_if_needed(transactions, as_dict)

    def get_transactions_by_sub_category(self, sub_category, as_dict=False):
        """
        Gets a list of all transactions matching a given sub_category.

        :param sub_category: sub_category of the transactions
        :param as_dict: (optional) if True, return a dictionary instead of a list of transactions
        :return: a list of transactions of the given sub_category
        """
        transactions = self.storage.load_transactions_by_sub_category(sub_category)

        return self._convert_if_needed(transactions, as_dict)

    def get_all_categories(self):
        return [
            {
                "category_name": cat.category_name,
                "sub_categories": cat.sub_categories,
                "is_income": cat.is_income
            }
            for cat in Category
        ]
