from datetime import datetime

class Transaction:
    """Defines a transaction."""
    def __init__(self, amount, category, sub_category, date=datetime.now()):
        self.amount = round(amount, 2)
        self.category = category
        self.sub_category = sub_category
        self.date = date