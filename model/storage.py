import sqlite3

class Storage:
    def __init__(self, db_name='finances.db'):
        self.db_name = db_name
        self._create_table_transactions()


    def _create_table_transactions(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def save_transaction(self, transaction):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO transactions (amount, description, category, date)
                VALUES (?, ?, ?, ?)''',
                           (transaction.amount, transaction.description, transaction.category, transaction.date))

            conn.commit()

    def load_all_transactions(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions''')

            return cursor.fetchall()

    def load_transactions_by_exact_date(self, date):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions WHERE date=?''',
                           (date,))

            return cursor.fetchall()

    def load_transactions_by_date_range(self, start_date, end_date):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions WHERE date>=? AND date<=?''',
                           (start_date,end_date))

            return cursor.fetchall()

    def load_transactions_by_from_date(self, start_date):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions WHERE date=?''',
                           (start_date,))

            return cursor.fetchall()

    def load_transactions_by_until_date(self, end_date):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions WHERE date=?''',
                           (end_date,))

            return cursor.fetchall()


    def load_transactions_by_category(self, category):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM transactions WHERE category = ?''',
                           (category,))

            return cursor.fetchall()

    def load_transactions_by_description(self, description):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions WHERE description = ?''',
                           (description,))

            return cursor.fetchall()
