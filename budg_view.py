import budg_controller as ctrl
from tabulate import tabulate

if __name__ == '__main__':
    print("This module cannot be run on it's own.")

class TransactionListView:
    def display_transactions(self, head, result):
        print(tabulate(result, headers = head, tablefmt = "rounded_grid", floatfmt=".2f"))

    def display_transactions_filtered(self, column = None, value = None):
        # TODO: should be allowing to select columns to filter on and values for that
        pass

class TransactionCreateView:
    def show_transaction_creation_result(self):
        # This should return the confirmation and the line that was added to table
        pass

class TransactionEditView:
    def show_transaction_update_result(self):
        # This should return the confirmation and the diff
        pass

class TransactionDeleteView:
    def show_transaction_delete_result(self):
        # This should return the confirmation and the line that was deleted
        pass
