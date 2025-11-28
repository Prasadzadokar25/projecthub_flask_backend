import json
from flask import make_response
from flask import request, jsonify
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
    
    
    def getCategories(self, uid):
        try:
            query = "SELECT category_id, category_name, category_description, image FROM categories"
            self.cur.execute(query)
            categories = self.cur.fetchall()
            return categories
        except pymysql.MySQLError as err:
            print(f"Database Error: {err}")
            return []