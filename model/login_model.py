import json
from flask import make_response
from flask import request, jsonify
import random
import string
import time
import pymysql
from werkzeug.security import check_password_hash
from model.db import get_db_connection, close_db_connection


class LoginModel:
    def __init__(self):
        """Initialize LoginModel with a centralized database connection."""
        self.con = get_db_connection()
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)
    
    def checkLoginDetailsModel(self, data):
        """Check login details and verify hashed password"""
        
        print(data)
        
        if 'user_key' not in data or 'user_password' not in data:
            res = {'status': 'False', 'message': "Username and password are required."}
            res = make_response(res, 400)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        
        if not data['user_key'] or not data['user_password']:
            res = {'status': 'False', 'message': "Username and password cannot be empty."}
            res = make_response(res, 400)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        
        user_key = data['user_key']
        password = data['user_password']
        
        query = """SELECT 
    u.user_id,
    u.user_name,
    u.user_password,
    u.user_description,
    u.loginType,
    u.country_code,
    u.phone_number,
    u.user_email,
    u.wallet_money,
    u.role,
    u.reference_code,
    u.profile_photo,
    u.created_at,
    IFNULL(bought_creations.bought_creation_number, 0) AS bought_creation_number,
    IFNULL(listed_creations.listed_creation_number, 0) AS listed_creation_number
FROM 
    users u
LEFT JOIN (
    SELECT 
        o.user_id,
        COUNT(o.order_id) AS bought_creation_number
    FROM 
        orders o
    GROUP BY 
        o.user_id
) AS bought_creations ON u.user_id = bought_creations.user_id
LEFT JOIN (
    SELECT 
        c.user_id,
        COUNT(c.creation_id) AS listed_creation_number
    FROM 
        creations c
    GROUP BY 
        c.user_id
) AS listed_creations ON u.user_id = listed_creations.user_id
WHERE 
    u.phone_number = %s;
"""
        
        try:
            self.cur.execute(query, (user_key,))
            result = self.cur.fetchone()
            
            if result:
                stored_password_hash = result['user_password']
                # Verify the hashed password
                if check_password_hash(stored_password_hash, password):
                    # Remove password from response for security
                    user_data = result.copy()
                    user_data.pop('user_password', None)
                    res = {
                        'status': 'success',
                        'data': user_data
                    }
                    res = make_response(res, 200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    return res
            
            res = {'status': 'False', 'message': "Invalid username or password."}
            res = make_response(res, 401)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        
        except pymysql.MySQLError as e:
            res = {'status': 'False', 'message': f"Database error: {str(e)}"}
            res = make_response(res, 500)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        except Exception as e:
            res = {'status': 'False', 'message': f"Error: {str(e)}"}
            res = make_response(res, 500)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res        