from datetime import datetime

class Transaction:
    def __init__(self, amount, description, category):
        self.amount = amount
        self.description = description
        self.category = category
        self.date = datetime.now()