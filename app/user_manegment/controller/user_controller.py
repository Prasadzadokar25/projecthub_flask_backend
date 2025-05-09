import os
import uuid
import pymysql
from flask import make_response
from flask import request, jsonify
import random
import string
import time

from app.database_connection.db_connection import get_db_connection

class UserController:
    
    def __init__(self):
        
        self.con = get_db_connection()
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)
        self.con.autocommit = True
            
    def generate_reference_code(self,length=6):
        timestamp = int(time.time())  # Current timestamp
        try:
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        except Exception as e:
            raise RuntimeError(f"Error generating reference code: {str(e)}")
        
        return f"{timestamp}{random_part}"

    def addUserModel(self, data):
        query = """
        INSERT INTO users (user_name, user_password, user_contact, role, reference_code)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            # Execute the insert query
            self.cur.execute(query, (data['user_name'], data['user_password'], data['user_contact'], data['role'], self.generate_reference_code()))

            # Fetch the last inserted ID
            self.cur.execute("SELECT LAST_INSERT_ID()")
            user_id = self.cur.fetchall()[0]['LAST_INSERT_ID()']

            # Commit the transaction
            self.con.commit()

            # Prepare the response
            res = make_response({"message": "User added successfully", "user_id": user_id}, 200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res

        except pymysql.MySQLError as e:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return make_response({"error": f"Database error: {str(e)}"}, 500)

        except Exception as e:
            # Handle any other exceptions
            return make_response({"error": f"Unexpected error: {str(e)}"}, 500)

        finally:
            # Ensure the cursor and connection are closed
            self.cur.close()
            self.con.close()



    def getUsersModel(self):
        query = "SELECT * FROM users"
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()

            if len(result) > 0:
                res = make_response({"data": result}, 200)
            else:
                res = make_response({"message": "No users found"}, 204)

            res.headers['Access-Control-Allow-Origin'] = "*"
            return res

        except pymysql.MySQLError as e:
            return make_response({"error": f"Database error: {str(e)}"}, 500)

        except Exception as e:
            return make_response({"error": f"Unexpected error: {str(e)}"}, 500)

        finally:
            # Ensure the cursor and connection are closed
            self.cur.close()
            self.con.close()

    def getUserByIdModel(self, id):
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
                    u.user_id = %s;
                """
        try:
            self.cur.execute(query, (id,))
            result = self.cur.fetchall()

            if len(result) > 0:
                res = make_response({"data": result[0]}, 200)
            else:
                res = make_response({"error": "No user found"}, 204)

            res.headers['Access-Control-Allow-Origin'] = "*"
            return res

        except pymysql.MySQLError as e:
            self.con.rollback()
            return make_response({"error": f"Database error: {str(e)}"}, 500)

        except Exception as e:
            self.con.rollback()
            return make_response({"error": f"Unexpected error: {str(e)}"}, 500)

        finally:
            self.cur.close()
            self.con.close()

    def checkNumberModel(self, number):
        query = "SELECT * FROM users WHERE user_contact = %s"
        try:
            self.cur.execute(query, (number,))
            result = self.cur.fetchall()

            if len(result) > 0:
                res = make_response({"userExist": "True"}, 200)
            else:
                res = make_response({"userExist": "False"}, 200)

            res.headers['Access-Control-Allow-Origin'] = "*"
            return res

        except pymysql.MySQLError as e:
            self.con.rollback()
            return make_response({"error": f"Database error: {str(e)}"}, 500)

        except Exception as e:
            return make_response({"error": f"Unexpected error: {str(e)}"}, 500)

        finally:
            self.cur.close()
            self.con.close()

    # Pagination in rest api
    def getUsersWitPaginationModel(self, limit, page):
        limit = int(limit)
        page = int(page)
        start = (limit * page) - limit

        query = f"SELECT * FROM userinfo LIMIT {start}, {limit}"
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()

            if len(result) > 0:
                res = make_response({"data": result}, 200)
            else:
                res = make_response({"message": "Data not found"}, 204)

            res.headers['Access-Control-Allow-Origin'] = "*"
            return res

        except pymysql.MySQLError as e:
            self.con.rollback()
            return make_response({"error": f"Database error: {str(e)}"}, 500)

        except Exception as e:
            return make_response({"error": f"Unexpected error: {str(e)}"}, 500)

        finally:
            self.cur.close()
            self.con.close()


    def updateUserModel(self, data):
        query = "UPDATE userInfo SET username = %s WHERE teacher_id = %s"
        try:
            # Execute the update query
            self.cur.execute(query, (data['name'], int(data['id'])))
            self.con.commit()

            if self.cur.rowcount > 0:
                return make_response({"message": "User updated successfully"}, 200)
            else:
                return make_response({"message": "Nothing to update"}, 204)

        except pymysql.MySQLError as e:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return make_response({"error": f"Database error: {str(e)}"}, 500)

        except Exception as e:
            return make_response({"error": f"Unexpected error: {str(e)}"}, 500)

        finally:
            # Ensure the cursor and connection are closed
            self.cur.close()
            self.con.close()

    def deleteUserModel(self, id):
        query = "DELETE FROM userInfo WHERE teacher_id = %s"
        try:
            # Execute the delete query
            self.cur.execute(query, (id,))
            self.con.commit()

            if self.cur.rowcount > 0:
                return make_response({"message": "User deleted successfully"}, 200)
            else:
                return make_response({"message": "Nothing to delete"}, 204)

        except pymysql.MySQLError as e:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return make_response({"error": f"Database error: {str(e)}"}, 500)

        except Exception as e:
            return make_response({"error": f"Unexpected error: {str(e)}"}, 500)

        finally:
            # Ensure the cursor and connection are closed
            self.cur.close()
            self.con.close()

    def uploadAvtarModel(self, id, filePath):
        query = "UPDATE userInfo SET avatr = %s WHERE teacher_id = %s"
        try:
            # Execute the update query
            self.cur.execute(query, (filePath, id))
            self.con.commit()

            if self.cur.rowcount > 0:
                return {"message": "File uploaded successfully"}
            else:
                return {"message": "File upload failed"}

        except pymysql.MySQLError as e:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return {"error": f"Database error: {str(e)}"}

        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

        finally:
            # Ensure the cursor and connection are closed
            self.cur.close()
            self.con.close()

    def update_user(self, user_id, data, files):
        if not data and 'profile_photo' not in files:
            return jsonify({"error": "No data provided"}), 400

        try:
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
                base_path = 'uploads/profilePick'
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

            # Execute the update query
            cursor.execute(update_query, values)
            connection.commit()

            return jsonify({"message": "User updated successfully", "updated_data": data}), 200

        except pymysql.MySQLError as e:
            # Rollback the transaction in case of an error
            connection.rollback()
            return jsonify({"error": f"Database error: {str(e)}"}), 500

        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

        finally:
            # Ensure the cursor and connection are closed
            if cursor:
                cursor.close()
            if connection:
                connection.close()


