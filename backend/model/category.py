from enum import Enum
from typing import List

class Category(Enum):
    """
    Enum of possible categories for transactions.
    Format: (category, sub_category, is_income)
    """
    def __init__(self, category_name: str, sub_categories: List[str], is_income: bool):
        self.category_name = category_name
        self.sub_categories = sub_categories
        self.is_income = is_income

    INCOME = ("Income", ['Job', 'Bonus', 'Part-time job', 'Child benefit', 'Housing benefit'], True)
    SALES = ("Sales", ['Vinted', 'kleinanzeigen', 'eBay'], True)
    FOOD = ("Food", ['Aleco', 'REWE', 'Rossmann', 'Bakery', 'Mensa'], False)
    HOME = ("Home", ['Rent', 'Electricity', 'Gas', 'GEZ', 'Internet', 'Insurance'], False)
    TRANSPORT = ("Transport", ['Bus', 'Tram', 'Cambio', 'Taxi', 'Train', 'Uber', 'Lime', 'Fairy', 'Airplane',], False)
    SPORT = ("Sport", ['Yoga', 'Swimming', 'Gym', 'Sports club'], False)
    HEALTH = ("Health", ['Doctor', 'Dentist', 'Pharmacy', 'Physiotherapy'], False)
    EDUCATION = ("Education", ['Library', 'Books', 'Semester fee'], False)
    PET = ("Pet", ['Pet food', 'Pet doctor', 'Pet training'], False)
    OTHER = ("Other", ['Clothes', 'Shoes', 'Gift', 'Holiday', 'Electronics'], False)

    @classmethod
    def get_all_categories(cls) -> List[object]:
        # returns all categories
        return [cat for cat in cls]

    @classmethod
    def from_category_as_string(cls, category_name: str):
        # returns category from category name
        for cat in cls:
            if cat.category_name == category_name:
                return cat
        return None



