from backend.model import Category

class Budget:
    """Defines a budget for a category."""
    def __init__(self, category: Category, limit: float, spent=0.0):
        self.category = category
        self.limit = limit
        self.spent = spent

    def add_expense(self, amount: float):
        self.spent += amount

    def get_remaining(self) -> float:
        return self.limit - self.spent
