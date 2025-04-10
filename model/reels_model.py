import pymysql
import json
from pymysql.cursors import DictCursor
from flask import make_response
from flask import request, jsonify
from pymysql.err import IntegrityError


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
                    SELECT * FROM (
                SELECT 
                    c.*,
                    (SELECT COUNT(*) FROM creation_likes cl WHERE cl.creation_id = c.creation_id) AS like_count,
                    (SELECT COUNT(*) FROM creation_shares cs WHERE cs.creation_id = c.creation_id) AS share_count,
                    EXISTS (
                        SELECT 1 FROM creation_likes cl 
                        WHERE cl.creation_id = c.creation_id AND cl.user_id = %s
                    ) AS is_liked_by_user
                FROM creations c
                WHERE c.youtube_link IS NOT NULL
                LIMIT %s OFFSET %s
            ) AS subquery
            ORDER BY RAND();

            """
            cursor.execute(query, (user_id, limit, offset))
            reels = cursor.fetchall()

            cursor.close()
            conn.close()
            return jsonify({"data":reels}),200
            

        except Exception as e:
            return  jsonify({"massage":f"server error:{e} "}),400


    def addLike(self, data):
        print(data)
        query = """
        INSERT INTO creation_likes (creation_id, user_id)
        VALUES (%s, %s)
        """
        values = (
            data['creation_id'],
            data['user_id']
        )

        try:
            self.cur.execute(query, values)
            self.con.commit()
            response = make_response({"message": "Like added successfully"}, 200)

        except pymysql.IntegrityError as e:
            self.con.rollback()

            if "unique_user_creation_like" in str(e):
                response = make_response({"message": "User has already liked this creation"}, 409)
            else:
                response = make_response({"message": "Database error", "error": str(e)}, 500)
                

        response.headers['Access-Control-Allow-Origin'] = "*"
        return response

        
    def removeLike(self,data):
        query = """
        delete from creation_likes where creation_id = %s AND user_id = %s
        """
        
        values = (
            data['creation_id'],
            data['user_id']
            
        )
        
        self.cur.execute(query, values)
        self.con.commit()
        responce = make_response({"message": "like removed sucessfuly"}, 200)
        responce.headers['Access-Control-Allow-Origin'] = "*"
        return responce
    
    def get_like_info(self, request):
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        reel_id = int(request.args.get('reel_id', 46))  # logged-in user
        try:
            conn = self.con
            cursor = self.cur
            
            query = """
                     SELECT 
                     u.user_id,
                    u.user_name,
                    u.user_description,
                    u.profile_photo
                FROM 
                    creation_likes cl
                JOIN 
                    users u ON cl.user_id = u.user_id
                WHERE 
                    cl.creation_id = %s
                ORDER BY 
                    cl.liked_at DESC
                LIMIT %s OFFSET %s;


            """
            values = (reel_id,limit,offset)
            cursor.execute(query,values)
            likes = cursor.fetchall()

            cursor.close()
            conn.close()
            return jsonify({"data":likes}),200
        
        except Exception as e:
            return  jsonify({"massage":f"server error:{e} "}),400