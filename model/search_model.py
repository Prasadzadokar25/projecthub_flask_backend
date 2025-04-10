import pymysql
import json
from pymysql.cursors import DictCursor
from flask import make_response
from flask import request, jsonify
from pymysql.err import IntegrityError

class SearchModel:
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
            
    def get_serched_Creations(self, request):
        limit = int(request.args.get('limit', 5))
        offset = int(request.args.get('offset', 0))
        user_query = request.args.get('user_query', "")  # search string

        try:
            conn = self.con
            cursor = self.cur

            # Add wildcards for LIKE
            search = f"%{user_query}%"

            query = """
                SELECT * FROM creations 
                WHERE (
                    creation_title LIKE %s OR
                    creation_description LIKE %s OR
                    keyword LIKE %s OR
                    creation_price LIKE %s OR
                    youtube_link LIKE %s
                )
                ORDER BY last_updated DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (search, search, search, search, search, limit, offset))
            searchedCreations = cursor.fetchall()

            cursor.close()
            conn.close()
            return jsonify({"data": searchedCreations}), 200

        except Exception as e:
            return jsonify({"message": f"Server error: {e}"}), 400
