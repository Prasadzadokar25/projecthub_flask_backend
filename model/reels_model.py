import pymysql
import json
from pymysql.cursors import DictCursor
from flask import make_response
from flask import request, jsonify

class ReelsModel :
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

    def get_reels(self, request):
        limit = int(request.args.get('limit', 5))
        offset = int(request.args.get('offset', 0))
        user_id = int(request.args.get('user_id', 46))  # logged-in user

        
        try:
            conn = self.con
            cursor = self.cur
            
            query = """
            SELECT 
                c.*,
                (SELECT COUNT(*) FROM creation_likes cl WHERE cl.creation_id = c.creation_id) AS like_count,
                (SELECT COUNT(*) FROM creation_shares cs WHERE cs.creation_id = c.creation_id) AS share_count,
                EXISTS (
                    SELECT 1 FROM creation_likes cl 
                    WHERE cl.creation_id = c.creation_id AND cl.user_id = %s
                ) AS is_liked_by_user
            FROM creations c
            WHERE c.youtube_link != 'null'
            ORDER BY RAND()
            LIMIT %s OFFSET %s
            """

            # query = """
            # SELECT c.*, 
            #     (SELECT COUNT(*) FROM creation_likes cl WHERE cl.creation_id = c.creation_id) AS like_count,
            #     (SELECT COUNT(*) FROM creation_shares cs WHERE cs.creation_id = c.creation_id) AS share_count
            # FROM creations c
            # WHERE c.youtube_link != 'null'
            # ORDER BY c.createtime DESC
            # LIMIT %s OFFSET %s
            # """
            cursor.execute(query, (user_id, limit, offset))
            reels = cursor.fetchall()

            cursor.close()
            conn.close()
            if(reels):
                return jsonify({"data":reels}),200
            return jsonify({"massage":"data not found"}),204

        except Exception as e:
            return  jsonify({"massage":f"server error:{e} "}),400
