from enum import Enum
from typing import List

class Category(Enum):
    # Format: (name, sub_category, is_income)
    def __init__(self, name: str, sub_categories: List[str], is_income: bool):
        self.name = name
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
    def get_all_names(cls) -> List[str]:
        # returns all category names as list
        return [cat.name for cat in cls]

    @classmethod
    def from_name(cls, name: str):
        # returns category from category name
        for cat in cls:
            if cat.name == name:
                return cat
        return None



