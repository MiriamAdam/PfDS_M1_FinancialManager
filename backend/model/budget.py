from backend.model import Category

class Budget:
    """Defines a budget for a category."""
    def __init__(self, category: Category, limit: float, spent=0.0):
        """
        Initializes a budget with:

        :param category: Name of the category.
        :param limit: Amount that limits the budget.

        """
        self.category = category
        self.limit = limit
        self.spent = spent

    def add_expense(self, amount: float):
        self.spent += amount

    def get_remaining(self):
        return self.limit - self.spent

    def reset_spent(self):
        self.spent = 0.0