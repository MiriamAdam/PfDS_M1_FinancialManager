from utils.db_creator import DbCreator
from view import ConsoleView

def main():
    creator = DbCreator()

    cui = ConsoleView()
    cui.start_financial_manager()
    creator.run_creator()

if __name__ == "__main__":
    main()