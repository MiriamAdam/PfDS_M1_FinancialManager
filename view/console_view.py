from controller import FinanceController

class ConsoleView:

    def __init__(self):
        self.fc = FinanceController()

    def show_start_menu(self):
        print('Start menu')
        print('Enter "1" to show transactions')
        print('Enter "2" to add a transaction')

    def start_financial_manager(self):
        self.show_start_menu()

        first_choice = input('Your selection: ')

        if first_choice == '1':
            print('Enter "1" to show all transactions')
            print('Enter "2" to show transactions by category')
            print('Enter "3" to show transactions by sub_category')
            print('Enter "4" to show transactions by date')

            second_choice = input('Your selection: ')

            if second_choice == '1':
                transactions = self.fc.get_all_transactions()
            elif second_choice == '2':
                category = input('Enter a category: ')
                transactions = self.fc.get_transactions_by_category(category)
            elif second_choice == '3':
                sub_category = input('Enter a sub-category: ')
                transactions = self.fc.get_transactions_by_sub_category(sub_category)
            elif second_choice == '4':
                exact_date = input('Enter a date: ')
                transactions = self.fc.get_transactions_by_date(exact_date)
            else:
                raise ValueError('Invalid input')

            if transactions:
                for transaction in transactions:
                    print(f'Category: {transaction.category_name}, Type: {transaction.sub_category}, Amount: {transaction.amount}€, Date: {transaction.date}\n')
            else:
                print('No transactions found')

        elif first_choice == '2':
            category = input('Enter a category: ')
            #category_name = category.from_name()
            sub_category = input('Enter a sub-category: ')
            amount = input('Enter amount: ')
            self.fc.add_transaction(category, sub_category, amount)