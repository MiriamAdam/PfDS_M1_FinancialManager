import os
import sqlite3

from backend.model import Transaction


class SqliteDb:
    def __init__(self, db_name='finances.db'):
        """
        Initializes database and creates finances.db in folder backend,
        transactions table and budget table if they don't exist.

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

    def load_all_transactions(self, start_date=None, end_date=None):
        """
        Retrieves all transactions from the database, optionally filtered by date range.
        :param start_date: (optional) start date of a timespan
        :param end_date: (optional) end date of a timespan
        :return: List of Transaction instances"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            conditions = []
            params = []

            if start_date:
                conditions.append("date >= ?")
                params.append(start_date)

            if end_date:
                conditions.append("date <= ?")
                params.append(end_date)

            query = "SELECT * FROM transactions"

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY date DESC"

            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

        return [Transaction(row[1], row[2], row[3], row[4]) for row in rows]

    def load_transactions_by_category(self, category_name, start_date=None, end_date=None):
        """
        Retrieves all transactions from the database by category, optionally filtered by date range.

        :param category_name: name of the category of the transactions
        :param start_date: (optional) start date of a timespan
        :param end_date: (optional) end date of a timespan
        :return: a list of transactions of the selected category
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM transactions WHERE category_name = ?"
            params = [category_name]

            if start_date:
                query += " AND date>=?"
                params.append(start_date)

            if end_date:
                query += " AND date<=?"
                params.append(end_date)

            query += " ORDER BY date DESC"

            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

        return [Transaction(row[1], row[2], row[3], row[4]) for row in rows]

    def load_transactions_by_sub_category(self, sub_category, start_date=None, end_date=None):
        """
        Retrieves all transactions from the database by sub category, optionally filtered by date range.

        :param sub_category: sub category of the transactions
        :param start_date: (optional) start date of a timespan
        :param end_date: (optional) end date of a timespan
        :return: a list of transactions of the selected sub category
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM transactions WHERE sub_category = ?"
            params = [sub_category]

            if start_date:
                query += " AND date>=?"
                params.append(start_date)

            if end_date:
                query += " AND date<=?"
                params.append(end_date)

            query += " ORDER BY date DESC"

            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

        return [Transaction(row[1], row[2], row[3], row[4]) for row in rows]

    def _create_table_budgets(self):
        """Creates budgets table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                category_name TEXT NOT NULL UNIQUE,
                'limit' REAL NOT NULL,
                last_reset_month text
            )
            ''')

            conn.commit()

    def save_budget(self, category_name: str, limit: float):
        """
        Saves a budget in database.

        :param category_name: name of the category of the budget
        :param limit: limit of the budget
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                   INSERT OR REPLACE INTO budgets (category_name, "limit")
                   VALUES (?, ?)''',
                   (category_name, limit))
            conn.commit()

    def get_budget_reset_month(self, category_name):
        """
        Gives last reset_month stamp of a budget.

        :param category_name: name of the category of the budget
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT last_reset_month FROM budgets WHERE category_name=?''',
                           (category_name,))
            row = cursor.fetchone()
            return row[0] if row else None

    def update_budget_reset_month(self, category_name, month):
        """
        Updates last_reset_month stamp.

        :param category_name: name of the category of the budget
        :param month: month of update
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE budgets SET last_reset_month = ? WHERE category_name = ?''',
                           (month, category_name))
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
            DELETE FROM budgets WHERE category_name = ?''', (category_name, ))
            conn.commit()