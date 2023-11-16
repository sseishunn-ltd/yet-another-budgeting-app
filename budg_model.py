import sqlite3
import budg_view as view

DB = "budget.db"
ERR_DB = "\nAn error occurred while working with the database:"
ERR_NON_DB = "Some error not related to database occured:"

if __name__ == '__main__':
    print("This module cannot be run on it's own.")

def tr_save(created_at, from_id, to_id, category_id, amount, comment):
    """Save transaction to the database."""
    con = None
    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()
        query = "INSERT INTO transactions_EUR \
                    (created_at, from_id, to_id, category_id, amount, comment) \
                VALUES (?, ?, ?, ?, ?, ?)"
        values = (created_at, from_id, to_id, category_id, amount, comment)
        cur.execute(query, values)
        con.commit()
    except sqlite3.Error as e:
        print(ERR_DB, str(e), "\n")
        status = False
        return status
    except Exception as e:
        print(ERR_NON_DB, str(e), "\n")
    finally:
        if cur:
            cur.close()
        if con:
            con.close()

def tr_delete_by_id(tr_id):
    """Delete the transaction from the database"""
    con = None
    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()
        query = "DELETE FROM transactions_EUR "
        query += f" WHERE transaction_id = {tr_id}"
        cur.execute(query)
        con.commit()
    except sqlite3.Error as e:
        print(ERR_DB, str(e), "\n")
        status = False
        return status
    except Exception as e:
        print(ERR_NON_DB, str(e), "\n")
    else:
        status = True
        return status
    finally:
        if cur:
            cur.close()
        if con:
            con.close()


def get_all(tr_id = None):
    """Retrieve all transactions from the database"""
    con = None
    try:
        con = sqlite3.connect(DB)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        #get table rows
        if tr_id == True:
            sql_query = """SELECT a.transaction_id as tr_id,
                        """
        else:
            sql_query = """SELECT
                        """
        sql_query += """
                        a.transaction_id, datetime(a.created_at, 'unixepoch') as datetime, 
                        b.category_name,
                        CAST(a.amount AS FLOAT) as amount,
                        c.account_name as acc_from,
                        d.account_name acc_to, 
                        a.comment
                    FROM
                        transactions_EUR as a
                        LEFT JOIN categories as b ON a.category_id = b.category_id
                        LEFT JOIN accounts as c ON a.from_id = c.account_id
                        LEFT JOIN accounts as d ON a.to_id = d.account_id
                    ORDER BY
                        a.transaction_id;
                    """

        cur.execute(sql_query)
        result = cur.fetchall()

        #get table headers
        head = result[0].keys()

        #get table footer
        if tr_id:
            sql_query = """SELECT NULL,
                        """
        else:
            sql_query = """SELECT
                        """
        sql_query += """
                        NULL,
                        NULL, 
                        'TOTAL', 
                        SUM(amount), 
                        NULL, 
                        NULL, 
                        NULL
                    FROM transactions_EUR
                    """
        cur.execute(sql_query)
        totals = cur.fetchone()
        result.append(totals)

        return head, result
    
    except sqlite3.Error as e:
        print(ERR_DB, str(e), "\n")
    except Exception as e:
        print(ERR_NON_DB, str(e), "\n")

    finally:
        if cur:
            cur.close()
        if con:
            con.close()

def get_categories():
    """Retrieve category names from the database"""
    con = None
    try:
        con = sqlite3.connect(DB)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        #get table rows
        sql_query = """
                    SELECT category_id, category_name
                    FROM categories
                    ORDER BY category_id;
                    """

        cur.execute(sql_query)
        result = cur.fetchall()

        return result
    
    except sqlite3.Error as e:
        print(ERR_DB, str(e), "\n")
    except Exception as e:
        print(ERR_NON_DB, str(e), "\n")

    finally:
        if cur:
            cur.close()
        if con:
            con.close()

def get_accounts():
    """Retrieve account names from the database"""
    con = None
    try:
        con = sqlite3.connect(DB)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        #get table rows
        sql_query = """
                    SELECT account_id, account_name
                    FROM accounts
                    ORDER BY account_id;
                    """

        cur.execute(sql_query)
        result = cur.fetchall()

        return result
    
    except sqlite3.Error as e:
        print(ERR_DB, str(e), "\n")
    except Exception as e:
        print(ERR_NON_DB, str(e), "\n")

    finally:
        if cur:
            cur.close()
        if con:
            con.close()