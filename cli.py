#!/usr/bin/env python3

import argparse
import budg_model as model
import budg_view as view
from datetime import datetime

def parse():
    # Parsing command line arguments
    parser = argparse.ArgumentParser(description="CLI tool to view and make records of transactions in budget.", add_help=True)
    subparsers = parser.add_subparsers(title = "Work with transactions", metavar=None, dest="subcommands")

    parser_read = subparsers.add_parser("read", help = "Get a list of all transactions from the record.")
    # TODO: parameter to filter by column
    parser_read.add_argument("--tail", metavar = "X", help="Show X last transactions")

    parser_add = subparsers.add_parser("add", help = "Add a new transaction to the record.")
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
        return None

    if args.subcommands.lower() == "add" and \
        all(value is None for key, value in vars(args).items() if key != "subcommands"):
        parser_add.print_help()
        return {}

    if args.subcommands.lower() == "edit" and \
        all(value is None for key, value in vars(args).items() if key != "subcommands"):
        parser_edit.print_help()
        return {}

    if args.subcommands.lower() == "delete" and \
        all(value is None for key, value in vars(args).items() if key != "subcommands"):
        parser_delete.print_help()
        return {}

    return args

def read_function(parsed_args):
    display_results = view.TransactionListView()
    if parsed_args.tail:
        head, result = model.Transaction.get_last_x(parsed_args.tail, 1)
        display_results.display_transactions(head, result)
    else:
        head, result = model.Transaction.get_all()
        display_results.display_transactions(head, result)

def add_function(parsed_args):
    # Get UNIX timestamp for date
    timestamp = int(datetime.timestamp(datetime.fromisoformat(parsed_args.timestamp))) \
        if parsed_args.timestamp else int(datetime.timestamp(datetime.today()))
    # TODO: get all necessary IDs for the shit provided from interface here
    trans = model.Transaction() # no params because we don't look up anything
    trans.save(created_at=timestamp, from_id=parsed_args.source_from, to_id=parsed_args.destination, \
        category_id=parsed_args.category, amount=parsed_args.amount, comment=parsed_args.comment)

def edit_function(parsed_args):
    trans = model.Transaction(transaction_id=parsed_args.tr_id, created_at=parsed_args.date, from_id=parsed_args.source_from, \
        to_id=parsed_args.destination, category_id=parsed_args.category, amount=parsed_args.amount, \
            comment=parsed_args.comment)
    trans.update(created_at=parsed_args.date_new, from_id=parsed_args.source_from_new, to_id=parsed_args.destination_new, \
        category_id=parsed_args.category_new, amount=parsed_args.amount_new, comment=parsed_args.comment_new)

# IMPORTANT: it only works by transaction for now
def delete_function(parsed_args):
    trans = model.Transaction(transaction_id=parsed_args.tr_id, created_at=None, from_id=parsed_args.source_from, \
        to_id=parsed_args.destination, category_id=parsed_args.category, amount=parsed_args.amount, \
            comment=parsed_args.comment)
    trans.delete()

def main():
    parsed_args = parse()

    if 'subcommands' in parsed_args:
        subcommand_functions = {
        'read': read_function,
        'add': add_function,
        'edit': edit_function,
        'delete': delete_function,
        }

        selected_function = subcommand_functions.get(parsed_args.subcommands.lower())

        if selected_function:
            selected_function(parsed_args)
        else:
            return

    # if parsed_args.subcommands.lower() == 'add':
    # if parsed_args.subcommands.lower() == 'edit':
    # if parsed_args.subcommands.lower() == 'delete':

    # Debug config
    # config = vars(parsed_args)
    # print("")
    # print(f"DEBUG: The arguments list: {config=}")


if __name__ == "__main__":
    #Run as main program
    main()