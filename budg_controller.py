import budg_model as model
import budg_view as view

if __name__ == '__main__':
    print("This module cannot be run on it's own.")

class TransactionController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def view_transactions(self, items = None):
        display_results = view.TransactionListView()
        if items:
            head, result = model.Transaction.get_last_x(items)
            display_results.display_transactions(head, result)
        else:
            head, result = model.Transaction.get_all()
            display_results.display_transactions(head, result)

    def view_filtered_transactions(self, column, value):
        # get entries filtered by columns and values in them
        pass

    def create_new_transaction(self, date, source_from, destination, category, amount, comment):
        # TODO: get all necessary IDs for the shit provided from interface here
        trans = model.Transaction() # no params because we don't look up anything
        trans.save(created_at=date, from_id=source_from, to_id=destination, category_id=category, amount=amount, comment=comment)

    def edit_transactions(self, tr_id, date, source_from, destination, category, amount, comment, date_new, \
        source_from_new, destination_new, category_new, amount_new, comment_new):
        trans = model.Transaction(transaction_id = tr_id, created_at = date, from_id = source_from, \
            to_id = destination, category_id = category, amount = amount, comment = comment)
        trans.update(created_at=date_new, from_id=source_from_new, to_id=destination_new, \
            category_id=category_new, amount=amount_new, comment=comment_new)

    def delete_transactions(self, tr_id, source_from, destination, category, amount, comment):
        trans = model.Transaction(transaction_id=tr_id, created_at=None, from_id=source_from, to_id=destination, \
            category_id=category, amount=amount, comment=comment)
        trans.delete()
