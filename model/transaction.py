from datetime import datetime

class Transaction:
    def __init__(self, amount, description, category):
        self.amount = round(amount, 2)
        self.description = description
        self.category = category
        self.date = datetime.now()