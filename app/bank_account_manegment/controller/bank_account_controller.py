from flask import jsonify, make_response
from app.database_connection.db_connection import get_db_connection

class BackAcountController:
    def add_bank_account(self, data):
        connection = get_db_connection()
        try:
            # Get the data from the request
            user_id = data['user_id']
            account_holder_name = data.get('account_holder_name')  # Optional
            bank_name = data['bank_name']
            account_number = data['account_number']
            ifsc_code = data['ifsc_code']

            # Validate required fields
            if not (user_id and bank_name and account_number and ifsc_code):
                response = make_response({'error': 'Missing required fields'}, 400)
                response.headers['Access-Control-Allow-Origin'] = "*"
                return response

            # Connect to the database
            with connection.cursor() as cursor:
                # Check for duplicate account number
                query = "SELECT * FROM bank_accounts WHERE account_number = %s AND user_id = %s"
                cursor.execute(query, (account_number, user_id))
                existing_account = cursor.fetchone()
                if existing_account:
                    return jsonify({'error': 'Account number already exists'}), 400

                # Check if this is the first account for the user
                query = "SELECT COUNT(*) AS account_count FROM bank_accounts WHERE user_id = %s"
                cursor.execute(query, (user_id,))
                account_count = cursor.fetchone()['account_count']

                # Set the new account as primary if it's the first account
                is_primary = account_count == 0  # True if this is the first account, False otherwise

                # Insert the bank account into the database
                query = """
                    INSERT INTO bank_accounts (user_id, account_holder_name, bank_name, account_number, ifsc_code, is_primary)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (user_id, account_holder_name, bank_name, account_number, ifsc_code, is_primary))
                connection.commit()

            return jsonify({'message': 'Bank account added successfully'}), 201

        except Exception as e:
            connection.rollback()
            # Handle any exceptions that occur during the process
            return jsonify({'error': str(e)}), 500
        finally:
             connection.close()
            

    def get_accounts_for_user(self,user_id):
        try:
            # Connect to the database
            connection = get_db_connection()
            print(user_id)
           
            with connection.cursor() as cursor:
                # Query to fetch all accounts for the given user_id
                query = """
                    SELECT *
                    FROM bank_accounts
                    WHERE user_id = %s;
                """
                cursor.execute(query, (user_id,))
                accounts = cursor.fetchall()

            # Close the connection
            # Check if accounts were found
            # if accounts:
            return jsonify({"status": "success", "data": accounts}), 200
            # else:
            #     return jsonify({"status": "error", "message": "No accounts found for the specified user"}), 404
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
        finally:
             connection.close()
    
    def set_primary_account(self,user_id, account_id):
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                # Step 1: Set all accounts for the user to is_primary = FALSE
                reset_query = """
                    UPDATE bank_accounts
                    SET is_primary = FALSE
                    WHERE user_id = %s
                """
                cursor.execute(reset_query, (user_id,))

                # Step 2: Set the specified account to is_primary = TRUE
                set_primary_query = """
                    UPDATE bank_accounts
                    SET is_primary = TRUE
                    WHERE account_id = %s AND user_id = %s
                """
                cursor.execute(set_primary_query, (account_id, user_id))

                # Commit the transaction
                connection.commit()

                return jsonify({"message": "Primary account updated successfully"}), 200
        except Exception as e:
            connection.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
             connection.close()