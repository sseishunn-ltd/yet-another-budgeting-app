#!/usr/bin/env python3

import curses
import budg_model as model
from tabulate import tabulate

def display_menu(stdscr):
    stdscr.clear()

    num_rows, num_cols = stdscr.getmaxyx()
    x_position = num_cols - 25
    y_position = 5
    
    options = ["Create Transaction", "Show Transactions", "Update Transaction", "Delete Transaction", "Exit"]
    selected_option = 0

    while True:
        stdscr.refresh()
        #curses.beep()
        
        stdscr.addstr(y_position,x_position, "======== MENU ========\n")
        for i, option in enumerate(options):
            if i == selected_option:
                stdscr.addstr(i+y_position+1, x_position, f"> {option}\n")
            else:
                stdscr.addstr(i+y_position+1, x_position, f"  {option}\n")
        stdscr.addstr(y_position+6,x_position, "======================\n")

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            head, result = process_user_choice(selected_option)
            stdscr.addstr(0,0,(tabulate(result, headers = head, tablefmt = "rounded_grid", floatfmt=".2f")))


def process_user_choice(choice):
    if choice == 0:
        pass
    elif choice == 1:
        head, result = model.Transaction.get_all()
        return head, result
    elif choice == 2:
        pass
    elif choice == 3:
        pass
    elif choice == 4:
        print("Exiting the application.")
        exit()


# Main user interface logic
def main(stdscr):
    curses.curs_set(0)
    display_menu(stdscr)

curses.wrapper(main)