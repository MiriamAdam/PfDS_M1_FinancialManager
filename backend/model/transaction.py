from datetime import datetime

class Transaction:
    """Defines a transaction."""
    def __init__(self, amount, category_name, sub_category, date=None):
        self.amount = round(amount, 2)
        self.category_name = category_name
        self.sub_category = sub_category
        if date is None:
            self.date = datetime.now()
        elif isinstance(date, str):
            try:
                self.date = datetime.fromisoformat(date)
            except ValueError:
                self.date = datetime.strptime(date, '%Y-%m-%d')
        else:
            self.date = date