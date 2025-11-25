from view import ConsoleView
from utils import TransactionCreator

def main():
    tc = TransactionCreator()
    #tc.create_random_transactions(100)
    cui = ConsoleView()
    cui.start_financial_manager()

if __name__ == "__main__":
    main()