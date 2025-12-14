from enum import Enum
from typing import List

class Category(Enum):
    """Enum of possible categories for transactions."""
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

    @property
    def category_name(self) -> str:
        """The display name of the main category (first element of the value tuple)."""
        return self.value[0]

    @property
    def sub_categories(self) -> List[str]:
        """List of sub-categories (second element of the value tuple)."""
        return self.value[1]

    @property
    def is_income(self) -> bool:
        """True if the category represents income (third element of the value tuple)."""
        return self.value[2]

    @classmethod
    def from_category_as_string(cls, category_name: str):
        """Searchs and returns category enum member from category_name. """
        for cat in cls:
            if cat.category_name == category_name:
                return cat
        return None



