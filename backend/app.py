import os
import sys
from backend.api.finance_api import app
from backend.db.db_creator import DbCreator
from backend.db.sqlite_db import SqliteDb

DB_NAME = "finances.db"

def setup_database_mode():
    """Asks user how to start app and initializes database."""

    print("\n--- Financial-Manager Setup ---\n")
    print("Choose how to start the app:")
    print("1: As new user with empty database")
    print("2: With new example transactions for testing")
    print("3: With already existing database")

    choice = ""
    while choice not in ('1', '2', '3', 'q'):
        choice = input("Choose 1, 2 or 3 (or q to quit): ")

    if choice.lower() == 'q':
        sys.exit(0)

    if choice == '3':
        if os.path.exists(DB_NAME):
            print(f"\nDatabase '{DB_NAME}' exists. Starting app...")
        else:
            print(f"\nDatabase does not exist. Creating new database...")
            SqliteDb(DB_NAME)
        return

    if os.path.exists(DB_NAME):
        print(f"\nDatabase '{DB_NAME}' already exists.")
        yesOrNo = ""
        while yesOrNo not in ('y', 'n'):
            yesOrNo = input("Do you want to delete the existing database? (y/n): ")

        if yesOrNo == 'y':
            os.remove(DB_NAME)
            print(f"Database '{DB_NAME}' deleted.")

        else:
            print("Use existing database. Starting app...")
            return

    if choice == '2':
        while True:
            years_str = input("For how many full years do you want to create transactions? ")
            try:
                years = int(years_str)
                if years > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a positive integer.")

        print("\nStart with testing data. Create database...")
        creator = DbCreator(years)
        creator.run_creator()
        print(f"Database with transactions for at least {years} years created.")

    # if choice is 1:
    else:
        print("\nStart as new user. Creating empty database...")
        SqliteDb(DB_NAME)
        print("Empty database created.")


if __name__ == '__main__':
    setup_database_mode()

    print("\nStarte Flask-Server...")
    app.run(debug=False, port=5000)