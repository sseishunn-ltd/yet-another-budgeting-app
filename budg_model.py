import sqlite3

DB = "budget.db"
ERR_DB = "\nAn error occurred while working with the database:"
ERR_NON_DB = "Some error not related to database occured:"
SUCCESS = "\nTransaction recorded successfully."

if __name__ == '__main__':
    print("This module cannot be run on it's own.")


class Transaction:
    """Methods for CRUD operations with the transaction entries. Lookup values go into object parameters, new values go into the method parameters."""
    def __init__(self, transaction_id=None, created_at=None, from_id=None, to_id=None, category_id=None, amount=None, comment=None):
        self.transaction_id = transaction_id
        self.created_at = created_at
        self.from_id = from_id
        self.to_id = to_id
        self.category_id = category_id
        self.amount = amount
        self.comment = comment

    # Methods for CRUD operations on transactions:
    def save(self, created_at, from_id, to_id, category_id, amount, comment):
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
        else:
            print(SUCCESS)
            status = True
            return status
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    # update_transactions(set_clauses, where_clauses)
    def update(self, created_at=None, from_id=None, to_id=None, category_id=None, amount=None, comment=None):
        """Update the transaction in the database"""
        con = None
        try:
            con = sqlite3.connect(DB)
            cur = con.cursor()
            query = """
                UPDATE transactions_EUR
                SET
                    created_at = COALESCE(?, created_at),
                    from_id = COALESCE(?, from_id),
                    to_id = COALESCE(?, to_id),
                    category_id = COALESCE(?, category_id),
                    amount = COALESCE(?, amount),
                    comment = COALESCE(?, comment)
                {}
            """
            conditions = [
               f"{column} = ?" for column in [
                    "transaction_id",
                    "created_at",
                    "from_id",
                    "to_id",
                    "category_id",
                    "amount",
                    "comment"
                ]
                if getattr(self, column) is not None
            ]
            where_clause = "WHERE " + " \n\t\tAND ".join(conditions) if conditions else ""
            query = query.format(where_clause) if where_clause else query
            values = [
                created_at,
                from_id,
                to_id,
                category_id,
                amount,
                comment]
            values = values + [
                getattr(self, column) for column in [
                    "transaction_id",
                    "created_at",
                    "from_id",
                    "to_id",
                    "category_id",
                    "amount",
                    "comment"
                ]
                if getattr(self, column) is not None
            ]
            cur.execute(query, values)
            con.commit()
        except sqlite3.Error as e:
            print(ERR_DB, str(e), "\n")
            status = False
            return status
        except Exception as e:
            print(ERR_NON_DB, str(e), "\n")
        else:
            print(SUCCESS)
            status = True
            return status
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    # delete_transactions(where_clauses)
    def delete(self):
        """Delete the transaction from the database"""
        con = None
        try:
            con = sqlite3.connect(DB)
            cur = con.cursor()
            query = "DELETE FROM transactions_EUR "
            conditions = [f"{column} = ?" for column in [
                    "transaction_id",
                    "created_at",
                    "from_id",
                    "to_id",
                    "category_id",
                    "amount",
                    "comment"
                ]
            if getattr(self, column) is not None
            ]
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            values = [value for value in (self.transaction_id, self.created_at, self.from_id, self.to_id, \
                self.category_id, self.amount, self.comment) if value is not None]
            cur.execute(query, values)
            con.commit()
        except sqlite3.Error as e:
            print(ERR_DB, str(e), "\n")
            status = False
            return status
        except Exception as e:
            print(ERR_NON_DB, str(e), "\n")
        else:
            print(SUCCESS)
            status = True
            return status
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    @staticmethod
    def get_all():
        """Retrieve all transactions from the database"""
        con = None
        try:
            con = sqlite3.connect(DB)
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            #get table rows
            cur.execute("""
                        SELECT datetime(a.created_at, 'unixepoch') as datetime, 
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
                        """)
            result = cur.fetchall()

            #get table headers
            head = result[0].keys()

            #get table footer
            cur.execute("""
                        SELECT 
                            NULL, 
                            'TOTAL', 
                            SUM(amount), 
                            NULL, 
                            NULL, 
                            NULL
                        FROM transactions_EUR
                        """)
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

    @staticmethod
    def get_last_x(items):
        """Retrieve last (items) transactions from the database"""
        con = None
        try:
            con = sqlite3.connect(DB)
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            #get table rows
            cur.execute(f"""
                        SELECT * FROM (
                            SELECT datetime(a.created_at, 'unixepoch') as datetime, 
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
                                a.transaction_id
                            DESC LIMIT {items})
                        ORDER BY
                            datetime ASC;
                        """)
            result = cur.fetchall()

            #get table headers
            head = result[0].keys()

            #get table footer
            cur.execute("""
                        SELECT 
                            NULL, 
                            'TOTAL', 
                            SUM(amount), 
                            NULL, 
                            NULL, 
                            NULL
                        FROM transactions_EUR
                        """)
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


class Category:
    #TODO: add CRUD methods for Category
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name


class Account:
    #TODO: add CRUD methods for Account
    def __init__(self, account_id, account_name):
        self.account_id = account_id
        self.account_name = account_name
