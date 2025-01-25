import pymysql
import json
from pymysql.cursors import DictCursor
from flask import make_response
from flask import request, jsonify
import random
import string
import time

class OrderModel:
    
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
    
    def create_order(self):
        try:
           
            # Insert into `payments` table
            payment_query = """
                INSERT INTO payments (
                    razorpay_order_id, razorpay_payment_id, razorpay_signature, 
                    payment_amount, gst_amount, platform_fee, payment_method, currency, 
                    transaction_id, status, payment_gateway_fee
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            payment_data = (
                'razorpay_order_123', 'razorpay_payment_456', 'signature_789',
                1000.00, 180.00, 50.00, 'credit_card', 'INR', 'txn_001', 
                'completed', 10.00
            )
            self.cur.execute(payment_query, payment_data)

            # Get the `payment_id` of the last inserted row
            payment_id = self.cur.lastrowid

            # Insert into `orders` table
            order_query = """
                INSERT INTO orders (user_id, payment_id) VALUES (%s, %s)
            """
            order_data = (47, payment_id)  # Example user_id = 1
            self.cur.execute(order_query,order_data)

            # Get the `order_id` of the last inserted row
            order_id = self.cur.lastrowid

            # Insert into `order_details` table
            order_details_query = """
                INSERT INTO order_details (order_id, creation_id, price, gst_amount, platform_fee)
                VALUES (%s, %s, %s, %s, %s)
            """
            order_details_data = [
                (order_id, 101, 500.00, 90.00, 25.00),  # Item 1
                (order_id, 120, 500.00, 90.00, 25.00)   # Item 2
            ]
            self.cur.executemany(order_details_query, order_details_data)

            # Commit the transaction
            self.con.commit()

            return jsonify({'message': 'Order created successfully', 'order_id': order_id}), 201

        except Exception as e:
            # Rollback the transaction on error
            self.con.rollback()
            return jsonify({'error': str(e)}), 500

        finally:
            # Close the cursor and connection
            self.cur.close()
            self.con.close()