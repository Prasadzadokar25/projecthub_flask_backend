import pymysql
import json
from pymysql.cursors import DictCursor
from flask import make_response
from flask import request, jsonify
class TransactionModel:
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
            
    def fetchTransaction(self,user_id):
        try:
            conn = self.con
            cursor = self.cur
            
            query = """
            SELECT 
                o.order_id,
                o.user_id,
                o.order_date,
                p.payment_id,
                p.razorpay_payment_id,
                p.payment_amount,
                p.gst_amount,
                p.platform_fee,
                p.payment_method,
                p.currency,
                p.transaction_date,
                p.status,
                p.payment_gateway_fee
            FROM 
                orders o
            JOIN 
                payments p ON o.payment_id = p.payment_id
            WHERE 
                o.user_id = %s
            ORDER BY 
                o.order_date DESC;
            """

            cursor.execute(query, (user_id))
            transactions = cursor.fetchall()

            cursor.close()
            conn.close()
            
            return jsonify({"data":transactions}),200
            

        except Exception as e:
            return  jsonify({"massage":f"server error:{e} "}),400