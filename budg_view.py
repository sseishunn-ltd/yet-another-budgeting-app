from tabulate import tabulate

#dummy

if __name__ == '__main__':
    print("This module cannot be run on it's own.")

class TransactionListView:
    def display_transactions(self, head, result):
        print("")
        print(tabulate(result, headers = head, tablefmt = "rounded_grid", floatfmt=".2f"))
    def display_transactions_filtered(self, column = None, value = None):
        # TODO: should be allowing to select columns to filter on and values for that
        pass

class TransactionCreateView:
    def show_transaction_creation_result(self, head, result):
        print("");
        print("The following line were added:")
        print(tabulate(result, headers = head, tablefmt = "rounded_grid", floatfmt=".2f"))

class TransactionEditView:
    # First render the line to be edited
    def show_transaction_update_attempt(self, head, result):
        print("");
        print("Attempting to edit the following line:")
        print(tabulate(result, headers = head, tablefmt = "rounded_grid", floatfmt=".2f"))
    # Then show the result
    def show_transaction_update_result(self, head, result):
        print("");
        print("The following edit was made:")
        print(tabulate(result, headers = head, tablefmt = "rounded_grid", floatfmt=".2f"))

class TransactionDeleteView:
    def show_transaction_delete_attempt(self, head, result):
        print("");
        print("Attempting to delete the following line:")
        print(tabulate(result, headers = head, tablefmt = "rounded_grid", floatfmt=".2f"))
    def show_transaction_delete_result(self):
        print("");
        print("Transaction deleted successfully.")