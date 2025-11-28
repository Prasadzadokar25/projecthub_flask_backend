import json
from flask import make_response
from flask import request, jsonify
from model.db import get_db_connection

class TransactionModel:
    def __init__(self):
        """Initialize TransactionModel with a centralized database connection."""
        self.con = get_db_connection()
        self.cur = self.con.cursor()
            
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