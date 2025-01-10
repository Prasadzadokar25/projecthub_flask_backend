import pymysql
import json
from pymysql.cursors import DictCursor
from flask import make_response
from flask import request, jsonify
import random
import string
import time

class LoginModel:
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
    
    def checkLoginDetailsModel(self,data):
        user_key = data['user_key']
        password = data['user_password']
        query = f"""SELECT 
    u.user_id,
    u.user_name,
    u.user_password,
    u.user_contact,
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
    u.user_contact = '{user_key}' or u.user_contact ='{user_key}';
""" 
        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result)>0:
            if result[0]['user_password'] == password:
                res = {
                        'status':'True',
                        'data':result
                    }
                res = make_response(res,200)
                res.headers['Access-Control-Allow-Origin']="*"
                return res
        res = {'status':'False','massage': "Invalid username or password."}
        res = make_response(res,401)
        res.headers['Access-Control-Allow-Origin']="*"
        return res        