from backend.model import Transaction, Category, SqliteDb
import random

class TransactionCreator:
    """
    helper class for creating transactions for testing
    """

    def __init__(self):
        self.storage = SqliteDb()

    def create_random_transactions(self, num_transactions: int):
        """
        creates random transactions and saves them in database

        :param num_transactions: number of transactions to create
        """
        for i in range(num_transactions):
            category = random.choice(list(Category))
            sub_category = random.choice(category.sub_categories)

            # income has bigger amounts than expenses
            if category.is_income:
                amount = round(random.uniform(1000, 5000), 2)
            else:
                amount = round(random.uniform(1, 500), 2)

            # creates a random string in datetime.now-format (day limited to 1-28 to always be valid)
            date = (f"2025-{random.randint(1, 12):02d}-{random.randint(1, 28):02d} "
                    f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}.000000")

            transaction = Transaction(amount, category.category_name, sub_category,  date)
            self.storage.save_transaction(transaction)