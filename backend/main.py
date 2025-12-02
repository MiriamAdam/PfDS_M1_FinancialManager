from backend.utils import DbCreator
from backend.view import ConsoleView

def main():
    creator = DbCreator()

    cui = ConsoleView()
    cui.start_financial_manager()
    creator.run_creator()

if __name__ == "__main__":
    main()