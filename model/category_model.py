import json
from flask import make_response
from flask import request, jsonify,current_app
import random
import string
import time
import pymysql
from model.db import get_db_connection

class categoryModel:
    
    def __init__(self):
        """Initialize categoryModel with a centralized database connection."""
        self.con = get_db_connection()
        self.cur = self.con.cursor()
    
    
    def getCategories(self, page, limit):
        try:
            base_url = current_app.config['BASE_URL']
            offset = (page - 1) * limit

            query = f"""
                SELECT 
                    category_id,
                    category_name,
                    category_description,
                    CONCAT('{base_url}/', image) AS image
                FROM categories
                LIMIT {limit} OFFSET {offset}
            """
            

            self.cur.execute(query)
            rows = self.cur.fetchall()

            # Count total categories
            self.cur.execute("SELECT COUNT(*) FROM categories")
            total = self.cur.fetchone()["COUNT(*)"]
            print("here")

            # categories = [{
            #     "category_id": row[0],
            #     "category_name": row[1],
            #     "category_description": row[2],
            #     "image": row[3]
            # } for row in rows]

            return rows, total

        except pymysql.MySQLError as err:
            print(f"DB Error: {err}")
            return [], 0
