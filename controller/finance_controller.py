from model import Transaction, Category, Storage

class FinancialController:
    def __init__(self):
        self.storage = Storage()

    def add_transaction(self, category: Category, description: str, amount: float):
        transaction = Transaction(category, description, amount)
        self.storage.save_transaction(transaction)

    def get_transaction_by_date(self, exact_date=None, start_date=None, end_date=None):
        # gets all transactions based on optional date parameters
        # without parameters: all transactions
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

    def get_transactions_by_category(self, category):
        return self.storage.load_transactions_by_category(category)

    def get_transactions_by_description(self, description):
        return self.storage.load_transactions_by_description(description)

