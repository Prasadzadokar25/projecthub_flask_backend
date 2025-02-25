import os
import uuid
import pymysql
import json
from pymysql.cursors import DictCursor
from flask import make_response
from flask import request, jsonify
import random
import string
import time

class UserModel:
    
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
            
    def generate_reference_code(self,length=6):
        timestamp = int(time.time())  # Current timestamp
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        return f"{timestamp}{random_part}"

    def addUserModel(self, data):
        query = """
        INSERT INTO users (user_name, user_password, user_contact, role, reference_code)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cur.execute(query, (data['user_name'], data['user_password'], data['user_contact'], data['role'], self.generate_reference_code()))

        # Fetch the last inserted ID
        self.cur.execute("SELECT LAST_INSERT_ID()")
        user_id = self.cur.fetchall()[0]['LAST_INSERT_ID()']

        self.con.commit()

        res = make_response({"message": "User added successfully", "user_id": user_id}, 200)
        res.headers['Access-Control-Allow-Origin'] = "*"
        return res



    def getUsersModel(self):
        qury = "select * from users"
        self.cur.execute(qury)
        result = self.cur.fetchall()
        #resultInStringFro = json.dumps(result)

        res = make_response({"data":result},200)
        res.headers['Access-Control-Allow-Origin']="*"
        return res

    def getUserByIdModel(self,id):
        query = f"""
                SELECT
                    u.user_id,
                    u.user_name,
                    u.user_contact,
                    u.user_description,
                    u.user_email,
                    u.wallet_money,
                    u.role,
                    u.reference_code,
                    u.profile_photo,
                    u.created_at,
                    u.loginType,
                    u.updated_at,
                    IFNULL(bought_creations.bought_creation_number, 0) AS bought_creation_number,
                    IFNULL(listed_creations.listed_creation_number, 0) AS listed_creation_number
                FROM
                    users u
                LEFT JOIN (
                    SELECT
                        o.user_id,
                        COUNT(od.order_detail_id) AS bought_creation_number
                    FROM
                        orders o
                    INNER JOIN
                        order_details od ON o.order_id = od.order_id
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
                    u.user_id = {id};
                """

        self.cur.execute(query)
        result = self.cur.fetchall()
        #resultInStringFro = json.dumps(result)
        if(len(result)>0):
            res = make_response({"data":result[0]},200)
            res.headers['Access-Control-Allow-Origin']="*"
            return res
        else:
            res = make_response({"error":"No user found"},204)
            res.headers['Access-Control-Allow-Origin']="*"
            return res

    def checkNumberModel(self,number):
        qury = f"select * from users where user_contact='{number}'"
        self.cur.execute(qury)
        result = self.cur.fetchall()
        if len(result)>0:
            res = make_response({"userExist":"True"},200)
        else:
            res = make_response({"userExist":"False"},200)
        res.headers['Access-Control-Allow-Origin']="*"
        return res

    # Pagination in rest api
    def getUsersWitPaginationModel(self,limit,page):

        limit = int(limit)
        page = int(page)
        start = (limit*page)-limit

        qury = f"select * from userinfo limit {start},{limit}"
        self.cur.execute(qury)
        result = self.cur.fetchall()
        #resultInStringFro = json.dumps(result)

        if len(result)>0:
            res = make_response({"data":result},200)
            res.headers['Access-Control-Allow-Origin']="*"
            return res
        else:
            res = make_response({"massage":"data not found"},204)
            res.headers['Access-Control-Allow-Origin']="*"
            return res


    def updateUserModel(self,data):
        query = f"update userInfo set username = '{data['name']}' where teacher_id={int(data['id'])}"
        self.cur.execute(query)
        self.con.commit()
        if  self.cur.rowcount>0:
            return "user updated succefuly"
        else:
            return "nottihing to update"

    def deleteUserModel(self,id):
        query = f"delete from userInfo where teacher_id={id}"
        self.cur.execute(query)
        self.con.commit()

        if  self.cur.rowcount>0:
            return "user deleted succefuly"
        else:
            return "nottihing to delete"

    def uploadAvtarModel(self,id,filePath):
        qry = f"Update userInfo Set avatr = '{filePath}' where teacher_id = {id}"
        self.cur.execute(qry)
        self.con.commit()

        if self.cur.rowcount>0:
            return {"maasage": "file uploaded succefuly"}
        else:
            return {"maasge":"file upload filled"}

    def update_user(self, user_id, data, files):
        if not data and 'profile_photo' not in files:
            return jsonify({"error": "No data provided"}), 400

        connection = self.con
        cursor = connection.cursor()

        fields = []
        values = []

        # Add user data to SQL query
        for key, value in data.items():
            fields.append(f"{key} = %s")
            values.append(value)

        # Handle profile photo upload
        if 'profile_photo' in files:
            base_path = 'uploads\profilePick'
            userProfilePhoto = files['profile_photo']
            unique_filename = str(uuid.uuid4()) + os.path.splitext(userProfilePhoto.filename)[1]
            file_path = os.path.join(base_path, unique_filename)

            # Save file
            userProfilePhoto.save(file_path)

            # Store path in database
            fields.append("profile_photo = %s")
            values.append(file_path)

        if not fields:
            return jsonify({"error": "No valid fields to update"}), 400

        # Append updated_at field
        fields.append("updated_at = CURRENT_TIMESTAMP")

        # Prepare SQL query
        update_query = f"UPDATE users SET {', '.join(fields)} WHERE user_id = %s"
        values.append(user_id)

        try:
            cursor.execute(update_query, values)
            connection.commit()
            return jsonify({"message": "User updated successfully", "updated_data": data}), 200
        except pymysql.MySQLError as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()


