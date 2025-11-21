from model import Category

class Budget:
    def __init__(self, category: Category, limit: float):
        self.category = category
        self.limit = limit
        self.spent = 0.0

    def add_expense(self, amount: float):
        self.spent += amount

    def get_remaining(self) -> float:
        return self.limit - self.spent
