import pymysql
from model.db import get_db_connection


class BankAccountModel:
    """Bank account data access model"""
    
    def __init__(self):
        self.con = get_db_connection()
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)
        self.con.autocommit = True

    def create_bank_account(self, user_id, account_holder_name, bank_name, account_number, ifsc_code):
        """Insert a new bank account"""
        query = """
        INSERT INTO bank_accounts (user_id, account_holder_name, bank_name, account_number, ifsc_code, is_primary)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            # Check for duplicate account number
            check_query = "SELECT * FROM bank_accounts WHERE account_number = %s AND user_id = %s"
            self.cur.execute(check_query, (account_number, user_id))
            existing_account = self.cur.fetchone()
            
            if existing_account:
                return {"success": False, "error": "Account number already exists"}

            # Check if this is the first account for the user
            count_query = "SELECT COUNT(*) AS account_count FROM bank_accounts WHERE user_id = %s"
            self.cur.execute(count_query, (user_id,))
            result = self.cur.fetchone()
            account_count = result['account_count'] if result else 0

            # Set the new account as primary if it's the first account
            is_primary = account_count == 0

            # Insert the bank account
            self.cur.execute(query, (user_id, account_holder_name, bank_name, account_number, ifsc_code, is_primary))
            self.con.commit()
            
            return {"success": True, "message": "Bank account added successfully"}
        except pymysql.MySQLError as e:
            self.con.rollback()
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def get_accounts_for_user(self, user_id):
        """Fetch all accounts for a user"""
        query = "SELECT * FROM bank_accounts WHERE user_id = %s"
        try:
            self.cur.execute(query, (user_id,))
            accounts = self.cur.fetchall()
            return {"success": True, "data": accounts}
        except pymysql.MySQLError as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def set_primary_account(self, user_id, account_id):
        """Set a specific account as primary for the user"""
        try:
            # Step 1: Set all accounts for the user to is_primary = FALSE
            reset_query = "UPDATE bank_accounts SET is_primary = FALSE WHERE user_id = %s"
            self.cur.execute(reset_query, (user_id,))

            # Step 2: Set the specified account to is_primary = TRUE
            set_primary_query = "UPDATE bank_accounts SET is_primary = TRUE WHERE account_id = %s AND user_id = %s"
            self.cur.execute(set_primary_query, (account_id, user_id))

            self.con.commit()
            return {"success": True, "message": "Primary account updated successfully"}
        except pymysql.MySQLError as e:
            self.con.rollback()
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def close(self):
        """Close database connection"""
        try:
            self.cur.close()
            self.con.close()
        except:
            pass
