import pymysql
from model.db import get_db_connection


class UserModel:
    """User data access model"""
    
    def __init__(self):
        self.con = get_db_connection()
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)
        self.con.autocommit = True

    def create_user(self, user_name, user_password, user_contact, role, reference_code):
        """Insert a new user into the database"""
        query = """
        INSERT INTO users (user_name, user_password, user_contact, role, reference_code)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.cur.execute(query, (user_name, user_password, user_contact, role, reference_code))
            self.cur.execute("SELECT LAST_INSERT_ID()")
            user_id = self.cur.fetchall()[0]['LAST_INSERT_ID()']
            self.con.commit()
            return {"success": True, "user_id": user_id}
        except pymysql.MySQLError as e:
            self.con.rollback()
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def get_all_users(self):
        """Fetch all users"""
        query = "SELECT * FROM users"
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()
            return {"success": True, "data": result if len(result) > 0 else None}
        except pymysql.MySQLError as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def get_user_by_id(self, user_id):
        """Fetch user by ID with statistics"""
        query = f"""
                SELECT
                    u.user_id,
                    u.user_name,
                    u.user_contact,
                    u.phone_number,
                    u.country_code,
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
            self.cur.execute(query, (user_id,))
            result = self.cur.fetchall()
            return {"success": True, "data": result[0] if len(result) > 0 else None}
        except pymysql.MySQLError as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def check_user_contact_exists(self, user_contact):
        """Check if phone number already exists"""
        query = "SELECT * FROM users WHERE user_contact = %s"
        try:
            self.cur.execute(query, (user_contact,))
            result = self.cur.fetchall()
            return {"success": True, "exists": len(result) > 0}
        except pymysql.MySQLError as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def get_users_paginated(self, limit, offset):
        """Fetch users with pagination"""
        query = f"SELECT * FROM users LIMIT {offset}, {limit}"
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()
            return {"success": True, "data": result if len(result) > 0 else None}
        except pymysql.MySQLError as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def update_user(self, user_id, update_data):
        """Update user information"""
        if not update_data:
            return {"success": False, "error": "No data provided"}
        
        fields = []
        values = []
        
        for key, value in update_data.items():
            fields.append(f"{key} = %s")
            values.append(value)
        
        fields.append("updated_at = CURRENT_TIMESTAMP")
        query = f"UPDATE users SET {', '.join(fields)} WHERE user_id = %s"
        values.append(user_id)
        
        try:
            self.cur.execute(query, values)
            self.con.commit()
            return {"success": True, "rowcount": self.cur.rowcount}
        except pymysql.MySQLError as e:
            self.con.rollback()
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def delete_user(self, user_id):
        """Delete a user"""
        query = "DELETE FROM users WHERE user_id = %s"
        try:
            self.cur.execute(query, (user_id,))
            self.con.commit()
            return {"success": True, "rowcount": self.cur.rowcount}
        except pymysql.MySQLError as e:
            self.con.rollback()
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def update_profile_photo(self, user_id, file_path):
        """Update user profile photo"""
        query = "UPDATE users SET profile_photo = %s, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s"
        try:
            self.cur.execute(query, (file_path, user_id))
            self.con.commit()
            return {"success": True, "rowcount": self.cur.rowcount}
        except pymysql.MySQLError as e:
            self.con.rollback()
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def close(self):
        """Close database connection"""
        try:
            self.cur.close()
            self.con.close()
        except:
            pass
