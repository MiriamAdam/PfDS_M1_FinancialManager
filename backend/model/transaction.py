from datetime import datetime

class Transaction:
    """Defines a financial transaction, including amount, name of category, sub category and date of transaction."""
    def __init__(self, amount, category_name, sub_category, date=None):
        """
        Initializes a new Transaction object.

        :param amount: Absolute amount of the transaction, rounded to 2 decimal places.
        :param category_name: Name of the main category.
        :param sub_category: Name of the specific sub category.
        :param date: Date and time of the transaction. If None defaults to current datetime. If a string, it attempts to parse it using either ISO format (YYYY-MM-DDTHH:MM:SS...)
                or the simple date format 'YYYY-MM-DD'. Defaults to None.
        """
        self.amount = round(abs(amount), 2)
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