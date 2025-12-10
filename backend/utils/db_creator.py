import sqlite3, random
from datetime import datetime, date


def add_random_time(dt):
    """Adds a random time to a given date."""
    return dt.replace(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
        microsecond=random.randint(0, 999999)
    ).strftime("%Y-%m-%d %H:%M:%S.%f")


class DbCreator:
    """Create new table 'transactions' with incomes/home and at least 20 random entries per month for other categories"""
    def __init__(self):
        self.db_name = "finances.db"

        self.start = date(2022, 1, 1)
        self.end = datetime.now().date()

        self.current = self.start
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category_name TEXT NOT NULL,
                sub_category TEXT NOT NULL,
                date TEXT NOT NULL
            )
            """)

    def add(self, amount, cat, sub, date):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO transactions (amount, category_name, sub_category, date) VALUES (?, ?, ?, ?)",
                (round(amount,2), cat, sub, date)
            )

    def run_creator(self):
        categories = {
            "Income": ["Job", "Bonus", "Part-time job", "Child benefit", "Housing benefit"],
            "Sales": ["Vinted", "kleinanzeigen", "eBay"],
            "Food": ["Aleco", "REWE", "Rossmann", "Bakery", "Mensa"],
            "Home": ["Rent", "Electricity", "Gas", "GEZ", "Internet", "Insurance"],
            "Transport": ["Bus", "Tram", "Cambio", "Taxi", "Train", "Uber", "Lime", "Fairy", "Airplane"],
            "Sport": ["Yoga", "Swimming", "Gym", "Sports club"],
            "Health": ["Doctor", "Dentist", "Pharmacy", "Physiotherapy"],
            "Education": ["Library", "Books", "Semester fee"],
            "Pet": ["Pet food", "Pet doctor", "Pet training"],
            "Other": ["Clothes", "Shoes", "Gift", "Holiday", "Electronics"]
        }

        while self.current <= self.end:
            y, m = self.current.year, self.current.month
            first_of_month = datetime(y, m, 1)
            # INCOME entries on 1st
            self.add(2900, "Income", "Job", add_random_time(first_of_month))
            self.add(500, "Income", "Child benefit", add_random_time(first_of_month))
            self.add(200, "Income", "Housing benefit", add_random_time(first_of_month))
            # part-time sometimes
            if random.random() < 0.35:
                self.add(random.uniform(100, 700), "Income", "Part-time job", add_random_time(first_of_month))
            # bonus in december
            if m == 12:
                self.add(1000, "Income", "Bonus", add_random_time(first_of_month))
            # HOME monthly at beginning
            self.add(1200, "Home", "Rent", add_random_time(first_of_month))
            self.add(random.uniform(50,80), "Home", "Electricity", add_random_time(first_of_month))
            self.add(random.uniform(30,60), "Home", "Gas", add_random_time(first_of_month))
            self.add(18.36, "Home", "GEZ", add_random_time(first_of_month))
            self.add(40, "Home", "Internet", add_random_time(first_of_month))
            self.add(random.uniform(40,90), "Home", "Insurance", add_random_time(first_of_month))
            # OTHER categories: at least 20 entries per month (distributed across categories)
            num_other = random.randint(20, 40)  # at least 20, up to 40 for variability
            other_keys = [k for k in categories.keys() if k not in ("Income", "Home")]
            for _ in range(num_other):
                cat = random.choice(other_keys)
                sub = random.choice(categories[cat])
                # choose amount ranges by category (positive for Sales)
                if cat == "Sales":
                    amt = random.uniform(5, 200)
                elif cat == "Food":
                    amt = random.uniform(3, 80)
                elif cat == "Transport":
                    amt = random.uniform(1, 60)
                elif cat == "Sport":
                    amt = random.uniform(5, 80)
                elif cat == "Health":
                    amt = random.uniform(5, 300)
                elif cat == "Education":
                    amt = random.uniform(5, 250)
                elif cat == "Pet":
                    amt = random.uniform(5, 200)
                else:  # Other
                    amt = random.uniform(5, 400)
                # random day in month (1-28 to be safe)
                day = random.randint(1,28)
                date_date = add_random_time(datetime(y, m, day))
                date_check = date(y, m, day)
                if date_check <= self.end:
                    self.add(amt, cat, sub, date_date)
            # move to next month
            if m == 12:
                self.current = date(y+1, 1, 1)
            else:
                self.current = date(y, m+1, 1)

            print("Generating for:", y, m)


