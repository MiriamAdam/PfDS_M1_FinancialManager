from controller import FinanceController

class ConsoleView:

    def __init__(self):
        self.fc = FinanceController()

    def print_start_menu(self):
        print('Start menu')
        print('Enter "1" to show transactions')
        print('Enter "2" to add a transaction')

    def print_show_transactions_menu(self):
        print('Enter "1" to show all transactions')
        print('Enter "2" to show transactions by category')
        print('Enter "3" to show transactions by sub_category')
        print('Enter "4" to show transactions by date')

    def print_what_date_menu(self):
        print('Enter "1" to show transactions of one day')
        print('Enter "2" to show transactions up to a specific date')
        print('Enter "3" to show transactions from a specific date onward')
        print('Enter "4" to show transactions of a date range')

    def print_return_transactions_by_date_menu(self):
        selected_option = input('Enter your choice: ')

        if selected_option == '1':
            return self.fc.get_transactions_by_date(input('Enter a date: '))
        elif selected_option == '2':
            return self.fc.get_transactions_by_date(input('Enter the date up to which you want to get transactions: '))
        elif selected_option == '3':
            return self.fc.get_transactions_by_date(input('Enter the date from which you want to see transactions up to now: '))
        elif selected_option == '4':
            start_date = input('Enter the start date of the timespan: ')
            end_date = input('Enter the end date of the timespan: ')
            return self.fc.get_transactions_by_date(start_date, end_date)
        else:
            raise ValueError('Invalid input')

    def print_selected_transactions(self, selected_choice: str):
        if selected_choice == '1':
            transactions = self.fc.get_all_transactions()
        elif selected_choice == '2':
            category = input('Enter a category: ')
            transactions = self.fc.get_transactions_by_category(category)
        elif selected_choice == '3':
            sub_category = input('Enter a sub-category: ')
            transactions = self.fc.get_transactions_by_sub_category(sub_category)
        elif selected_choice == '4':
            self.print_what_date_menu()
            transactions = self.print_return_transactions_by_date_menu()
        else:
            raise ValueError('Invalid input')

        if transactions:
            for transaction in transactions:
                print(
                    f'Category: {transaction.category_name}, Type: {transaction.sub_category}, Amount: {transaction.amount}€, Date: {transaction.date}\n')
        else:
            print('No transactions found')

    def add_transaction(self):
        category_name = input('Enter a category: ')
        sub_category = input('Enter a sub-category: ')
        amount = input('Enter amount: ')
        amount = float(amount)
        self.fc.add_transaction(amount, category_name, sub_category)

    def start_financial_manager(self):
        self.print_start_menu()

        first_choice = input('Your selection: ')

        if first_choice == '1':
            self.print_show_transactions_menu()

            second_choice = input('Your selection: ')

            self.print_selected_transactions(second_choice)

        elif first_choice == '2':
            self.add_transaction()