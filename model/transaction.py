from datetime import datetime

class Transaction:
    def __init__(self, amount, sub_category, category, date=datetime.now()):
        self.amount = round(amount, 2)
        self.sub_category = sub_category
        self.category = category
        self.date = date