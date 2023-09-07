#!/usr/bin/env python3

import argparse
import budg_model as model
import budg_view as view
from datetime import datetime

def main():

    # Parsing command line arguments
    parser = argparse.ArgumentParser(description="CLI tool to view and make records of transactions in budget.", add_help=True)
    subparsers = parser.add_subparsers(title = "Work with transactions", metavar=None, dest="subcommands")

    parser_read = subparsers.add_parser("read", help = "Get a list of all transactions from the record.")
    # TODO: show only X last transactions
    # TODO: parameter to set X of shown transactions
    # TODO: parameter to filter by column
    parser_read.add_argument("--tail", metavar = "X", help="Show X last transactions")

    parser_add = subparsers.add_parser("add", help = "Add a new transaction to the record.")
    # TODO: add date to parameters
    # TODO: a way to show transactions between two time points
    parser_add.add_argument("--timestamp", help="Date in YYYY-MM-DD format, time will be set to 00:00.")
    parser_add.add_argument("source_from", help="Source account or payee. If no matching entity is found, transaction \
        will not be recorded.")
    parser_add.add_argument("destination", help="Destination account or payee. If no matching entity is found, a \
        new one will be created.")
    parser_add.add_argument("category", help="Category to which the transaction is attributed. If no matching entity \
        is found, transaction will not be recorded.")
    parser_add.add_argument("amount", type=float, help="Amount of the transaction in your default currency. Positive \
        figures are income, negative are expenses.")
    parser_add.add_argument("--comment", help="Comment, not mandatory.", default=None)

    parser_edit = subparsers.add_parser("edit", help = "Update transaction: provide lookup values (for AND conjunction), \
        and new values to be set in the found entries. Note that you cannot change Transaction ID.", add_help=True)
    parser_edit.add_argument("--tr_id", help="Transaction ID used for lookup.")
    # TODO: treat dates properly here:
    parser_edit.add_argument("--date", help="Date to be used for lookup, needs to be an UNIX timestamp (for now).")
    parser_edit.add_argument("--source_from", help="Source account or payee used for lookup.")
    parser_edit.add_argument("--destination", help="Destination account or payee used for lookup.")
    parser_edit.add_argument("--category", help="Category to which the transaction is attributed used for lookup.")
    parser_edit.add_argument("--amount", type=float, help="Amount of the transaction used for lookup.")
    parser_edit.add_argument("--comment", help="Comment used for lookup.")
    parser_edit.add_argument("--date_new", help="New Date to be set on looked up entries, needs to be an UNIX timestamp.")
    parser_edit.add_argument("--source_from_new", help="New Source account or payee to be set on looked up entries.")
    parser_edit.add_argument("--destination_new", help="New Destination account or payee to be set on looked up entries.")
    parser_edit.add_argument("--category_new", help="New Category to which the transaction is attributed to be set \
        on looked up entries.")
    parser_edit.add_argument("--amount_new", type=float, help="New Amount of the transaction to be set on looked up \
        entries.")
    parser_edit.add_argument("--comment_new", help="New Comment to be set on looked up entries.")

    parser_delete = subparsers.add_parser("delete", help = "Delete transaction - looked up by provided parameter values. \
        If no parameters are set, all transactions will be deleted!")
    parser_delete.add_argument("--tr_id", help="Transaction ID.")
    parser_delete.add_argument("--source_from", help="Source account or payee.")
    parser_delete.add_argument("--destination", help="Destination account or payee.")
    parser_delete.add_argument("--category", help="Category to which the transaction is attributed.")
    parser_delete.add_argument("--amount", type=float, help="Amount of the transaction.")
    parser_delete.add_argument("--comment", help="Comment.")

    args = parser.parse_args()
        
    if args.subcommands == None:
        parser.print_help()
        return

    if args.subcommands.lower() == "add" and \
        all(value is None for key, value in vars(args).items() if key != "subcommands"):
        parser_add.print_help()
        return

    if args.subcommands.lower() == "edit" and \
        all(value is None for key, value in vars(args).items() if key != "subcommands"):
        parser_edit.print_help()
        return

    if args.subcommands.lower() == "delete" and \
        all(value is None for key, value in vars(args).items() if key != "subcommands"):
        parser_delete.print_help()
        return

    # Get UNIX timestamp for date
    # TODO: parse timestamp from parameters and use it if provided!
    if args.subcommands.lower() == "add":
        try:
            dt_input = datetime.fromisoformat(args.timestamp)
            timestamp = int(datetime.timestamp(dt_input))
        except:
            dt_input = datetime.today()
            timestamp = int(datetime.timestamp(dt_input))

    if args.subcommands.lower() == 'read':
        display_results = view.TransactionListView()
        if args.tail:
            head, result = model.Transaction.get_last_x(args.tail)
            display_results.display_transactions(head, result)
        else:
            head, result = model.Transaction.get_all()
            display_results.display_transactions(head, result)

    if args.subcommands.lower() == 'add':
        # TODO: get all necessary IDs for the shit provided from interface here
        trans = model.Transaction() # no params because we don't look up anything
        trans.save(created_at=timestamp, from_id=args.source_from, to_id=args.destination, category_id=args.category, \
            amount=args.amount, comment=args.comment)

    if args.subcommands.lower() == 'edit':
        trans = model.Transaction(transaction_id=args.tr_id, created_at=args.date, from_id=args.source_from, \
            to_id=args.destination, category_id=args.category, amount=args.amount, comment=args.comment)
        trans.update(created_at=args.date_new, from_id=args.source_from_new, to_id=args.destination_new, \
            category_id=args.category_new, amount=args.amount_new, comment=args.comment_new)

    if args.subcommands.lower() == 'delete':
        trans = model.Transaction(transaction_id=args.tr_id, created_at=None, from_id=args.source_from, to_id=args.destination, \
            category_id=args.category, amount=args.amount, comment=args.comment)
        trans.delete()

    # Debug config
    config = vars(args)
    print(f"The arguments list: {config=}")

if __name__ == "__main__":
    #Run as main program
    main()