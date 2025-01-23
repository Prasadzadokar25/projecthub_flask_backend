import pymysql
import json
from pymysql.cursors import DictCursor
from flask import jsonify, make_response

class BackAcountModel:
    def __init__(self):
        
        # local server
        host = "localhost"        
        user = "root"
        password = "##Prasad25"
        database = "projecthubdb"
        
        # # pythonanywhere server 
        # host = "projecthub.mysql.pythonanywhere-services.com"
        # user = "projecthub"
        # password = "##Prasad25"
        # database = "projecthub$projecthubdb"
        try:
            self.con = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                cursorclass=DictCursor
            )
            self.con.autocommit = True
            self.cur = self.con.cursor()
            print("connect succefuly")
        except pymysql.MySQLError as err:
            print(f"Failed to connect: {err}")
            
    def add_bank_account(self,data):
        try:
            # Get the data from the request
            user_id = data['user_id']
            account_holder_name = data['account_holder_name']  # Optional
            bank_name = data['bank_name']
            account_number = data['account_number']
            ifsc_code = data['ifsc_code']

            # Validate required fields
            if not (user_id and bank_name and account_number and ifsc_code):
                responce = make_response({'error': 'Missing required fields'}, 400)
                responce.headers['Access-Control-Allow-Origin'] = "*"
                return responce
                #return jsonify({'error': 'Missing required fields'}), 400

            # Connect to the database
            with self.con.cursor() as cursor:
                # Check for duplicate account number
                query = "SELECT * FROM bank_accounts WHERE account_number = %s and user_id = %s"
                cursor.execute(query, (account_number,user_id))
                existing_account = cursor.fetchone()
                if existing_account:
                    return jsonify({'error': 'Account number already exists'}), 400

                # Insert the bank account into the database
                query = """
                    INSERT INTO bank_accounts (user_id, account_holder_name, bank_name, account_number, ifsc_code)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (user_id, account_holder_name, bank_name, account_number, ifsc_code))
                self.con.commit()
            
            responce = make_response({'message': 'Bank account added successfully'}, 201)
            responce.headers['Access-Control-Allow-Origin'] = "*"
            return responce
            return jsonify({'message': 'Bank account added successfully'}), 201

        except Exception as e:
            responce = make_response({'error': str(e)}, 500)
            responce.headers['Access-Control-Allow-Origin'] = "*"
            return responce
           # return jsonify({'error': str(e)}), 500
           
    def get_accounts_for_user(self,user_id):
        try:
            # Connect to the database
           
            with self.con.cursor() as cursor:
                # Query to fetch all accounts for the given user_id
                query = """
                    SELECT account_id, account_holder_name, bank_name, account_number, ifsc_code, created_at, updated_at
                    FROM bank_accounts
                    WHERE user_id = %s;
                """
                cursor.execute(query, (user_id,))
                accounts = cursor.fetchall()

            # Close the connection
            self.con.close()
            # Check if accounts were found
            if accounts:
                return jsonify({"status": "success", "data": accounts}), 200
            else:
                return jsonify({"status": "error", "message": "No accounts found for the specified user"}), 404
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500