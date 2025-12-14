from datetime import datetime

class Transaction:
    """
    Defines a single financial transaction.

    This class stores all essential information about a monetary transaction:
    the amount, the date, and the associated categories
    (main category and sub-category).
    """
    def __init__(self, amount, category_name, sub_category, date=None):
        """
        Initializes a new Transaction object.

        The amount is always stored as a positive value (absolute amount) and rounded to two decimal places.

        :param amount: Absolute amount of the transaction, rounded to 2 decimal places.
        :param category_name: Name of the main category.
        :param sub_category: Name of the specific sub category.
        :param date: The date and time of the transaction (datetime.datetime, string, or None). Defaults to None.
        If None, the current datetime.now() is used.
        If a string, the method attempts to parse it as a datetime object, using either the ISO format
        (e.g., 'YYYY-MM-DDTHH:MM:SS') or the simple date format ('YYYY-MM-DD').
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