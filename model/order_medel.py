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
    
    def create_order(self, data):
        user_id = data['user_id']
        payment_data = data['payment_details']  # This should be from the request body
        products = data['product']  # List of products in the order
        
        try:
            # Insert into `payments` table
            payment_query = """
                INSERT INTO payments (
                     razorpay_payment_id,
                    payment_amount, gst_amount, platform_fee, payment_method, currency, 
                    status, payment_gateway_fee
                ) VALUES ( %s, %s,   %s, %s, %s, %s, %s, %s)
            """
            payment_data_values = (
               payment_data['razorpay_payment_id'], 
                payment_data['payment_amount'], payment_data['gst_amount'], payment_data['platform_fee'], payment_data['payment_method'], 
                payment_data['currency'], payment_data['status'], payment_data['payment_gateway_fee']
            )
            self.cur.execute(payment_query, payment_data_values)

            # Get the `payment_id` of the last inserted row
            payment_id = self.cur.lastrowid

            # Insert into `orders` table
            order_query = """
                INSERT INTO orders (user_id, payment_id) VALUES (%s, %s)
            """
            order_data = (user_id, payment_id)
            self.cur.execute(order_query, order_data)

            # Get the `order_id` of the last inserted row
            order_id = self.cur.lastrowid

            # Prepare `order_details` data
            order_details_query = """
                INSERT INTO order_details (order_id, creation_id, price, gst_amount, platform_fee)
                VALUES (%s, %s, %s, %s, %s)
            """
            update_wallet_query = """
                Update users
                set wallet_money = wallet_money+%s
                where user_id = %s
            """
            order_details_data = []
            for product in products:
                net_earning = product['price']
                self.cur.execute(update_wallet_query, (net_earning, product['seller_id']))

                print(product['seller_id'])
                order_details_data.append((
                    order_id, product['creation_id'], product['price'], product['gst_amount'], product['platform_fee']
                ))
                
            
            # Insert the order details
            self.cur.executemany(order_details_query, order_details_data)

            unmark_cart_query = """
            UPDATE carditems
            SET status = 0
            WHERE user_id = %s
              AND creation_id IN (SELECT creation_id FROM order_details WHERE order_id = %s)
        """
            self.cur.execute(unmark_cart_query, (user_id, order_id))
            
        # Increment the `total_copy_sell` for each creation sold
            increment_sell_query = """
                UPDATE creations
                SET total_copy_sell = total_copy_sell + 1
                WHERE creation_id IN (SELECT creation_id FROM order_details WHERE order_id = %s)
            """
            self.cur.execute(increment_sell_query, (order_id,))

        # Commit the transaction
            self.con.commit()
            
            


            return jsonify({'message': 'Order created successfully', 'order_id': order_id}), 201

        except Exception as e:
            # Rollback the transaction on error
            self.con.rollback()
            return jsonify({'error': f"An error occurred: {str(e)}"}), 500

        finally:
            # Close the cursor and connection
            if hasattr(self, 'cur') and self.cur:
                self.cur.close()
            if hasattr(self, 'con') and self.con:
                self.con.close()
