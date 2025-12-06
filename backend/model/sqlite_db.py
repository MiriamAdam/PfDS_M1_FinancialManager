import sqlite3

from backend.model import Transaction


class SqliteDb:
    def __init__(self, db_name='finances.db'):
        """
        Initializes database and creates transactions table and budget table if it doesn't exist.

        :param db_name: Name of the SQLite database file (default: finances.db)
        """
        self.db_name = db_name
        self._create_table_transactions()
        self._create_table_budgets()


    def _create_table_transactions(self):
        """Creates transactions table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category_name TEXT NOT NULL,
                    sub_category TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            ''')

            conn.commit()

    def save_transaction(self, transaction):
        """
        Saves a Transaction object into the database.

        :param transaction: Transaction instance to save
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO transactions (amount, category_name, sub_category, date)
                VALUES (?, ?, ?, ?)''',
                           (transaction.amount, transaction.category_name, transaction.sub_category, transaction.date))

            conn.commit()

    def load_all_transactions(self):
        """
        Retrieves all transactions from the database.
        :return: List of Transaction instances"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions ORDER BY date DESC''')

            rows = cursor.fetchall()

        return [Transaction(row[1], row[2], row[3], row[4]) for row in rows]

    def load_transactions_by_exact_date(self, date):
        """
        Retrieves all transactions from the database by the given date.

        :param date: date of the transaction
        :return: a list of transactions from the given date
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions WHERE date=?''',
                           (date,))

            rows = cursor.fetchall()

        return [Transaction(row[1], row[2], row[3], row[4]) for row in rows]

    def load_transactions_by_date_range(self, start_date, end_date):
        """
        Retrieves all transactions from the database by the given date range.

        :param start_date: start date of a timespan
        :param end_date: end date of a timespan
        :return: a list of transactions in the given date range
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions WHERE date>=? AND date<=?''',
                           (start_date,end_date))

            rows = cursor.fetchall()

        return [Transaction(row[1], row[2], row[3], row[4]) for row in rows]

    def load_transactions_by_from_date(self, start_date):
        """
        Retrieves all transactions from the database from the given date onward.

        :param start_date: start date of a timespan
        :return: a list of transactions starting from the given date onward
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions WHERE date>=?''',
                           (start_date,))

            rows = cursor.fetchall()

        return [Transaction(row[1],row[2], row[3], row[4]) for row in rows]

    def load_transactions_by_until_date(self, end_date):
        """
        Retrieves all transactions from the database upto the given date.

        :param end_date: end date of a timespan
        :return: a list of transactions upto the given date
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions WHERE date<=?''',
                           (end_date,))

            rows = cursor.fetchall()

        return [Transaction(row[1], row[2], row[3], row[4]) for row in rows]


    def load_transactions_by_category(self, category_name):
        """
        Retrieves all transactions from the database by category.

        :param category_name: name of the category of the transactions
        :return: a list of transactions of the selected category
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM transactions WHERE category_name = ?''',
                           (category_name,))

            rows = cursor.fetchall()

        return [Transaction(row[1], row[2], row[3], row[4]) for row in rows]

    def load_transactions_by_sub_category(self, sub_category):
        """
        Retrieves all transactions from the database by sub category.

        :param sub_category: sub category of the transactions
        :return: a list of transactions of the selected sub category
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM transactions WHERE sub_category = ?''',
                           (sub_category,))

            rows = cursor.fetchall()

        return [Transaction(row[1], row[2], row[3], row[4]) for row in rows]

    def _create_table_budgets(self):
        """Creates budgets table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                category_name TEXT NOT NULL UNIQUE,
                'limit' REAL NOT NULL
            )
            ''')

            conn.commit()

    def save_budget(self, category_name: str, limit: float):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                   INSERT OR REPLACE INTO budgets (category_name, "limit")
                   VALUES (?, ?)''',
                   (category_name, limit))
            conn.commit()

    def load_all_budgets(self):
        """
        Retrieves all budgets from the database.
        :return: Dictionary with category_name as key and limit as value
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT category_name, "limit" FROM budgets')
            rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}

    def delete_budget(self, category_name: str):
        """Deletes a budget from the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            DELETE FROM budgets WHERE category_name = ?''', category_name)
            conn.commit()