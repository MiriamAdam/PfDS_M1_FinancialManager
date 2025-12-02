from datetime import datetime

class Transaction:
    """Defines a transaction."""
    def __init__(self, amount, category_name, sub_category, date=datetime.now()):
        self.amount = round(amount, 2)
        self.category_name = category_name
        self.sub_category = sub_category
        self.date = date