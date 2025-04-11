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

            search = f"%{user_query}%"

            query = """
                SELECT 
                    c.creation_id,
                    c.creation_title,
                    c.creation_description,
                    c.creation_price,
                    c.creation_thumbnail,
                    c.creation_file,
                    c.category_id,
                    c.keyword,
                    c.createtime,
                    c.creation_other_images,
                    c.total_copy_sell,
                    c.youtube_link,
                    c.last_updated,

                    u.user_id AS seller_id,
                    u.user_name AS seller_name,
                    u.user_email AS seller_email,
                    u.profile_photo AS seller_profile_photo,

                    COALESCE(AVG(r.rating), 0) AS average_rating,
                    COUNT(r.rating_id) AS number_of_reviews,

                    (
                        (c.creation_title LIKE %s) +
                        (c.creation_description LIKE %s) +
                        (c.keyword LIKE %s) +
                        (c.creation_price LIKE %s) +
                        (c.youtube_link LIKE %s)
                    ) AS match_score

                FROM creations c
                JOIN users u ON c.user_id = u.user_id
                LEFT JOIN ratings r ON c.creation_id = r.creation_id

                WHERE 
                    (
                        u.user_name LIKE %s OR
                        c.creation_title LIKE %s OR
                        c.creation_description LIKE %s OR
                        c.keyword LIKE %s OR
                        c.creation_price LIKE %s OR
                        c.youtube_link LIKE %s
                    )

                GROUP BY c.creation_id, u.user_id
                ORDER BY match_score DESC, c.last_updated DESC
                LIMIT %s OFFSET %s;
            """

            cursor.execute(query, (
                search, search, search, search, search,search,
                search, search, search, search, search,
                limit, offset
            ))

            rows = cursor.fetchall()
            result_list = []

            for row in rows:
                result_list.append({
                    "average_rating": float(row["average_rating"]),
                    "category_id": row["category_id"],
                    "createtime": row["createtime"].strftime('%a, %d %b %Y %H:%M:%S GMT'),
                    "creation_description": row["creation_description"],
                    "creation_file": row["creation_file"],
                    "creation_id": row["creation_id"],
                    "creation_other_images": row["creation_other_images"],
                    "creation_price": str(row["creation_price"]),
                    "creation_thumbnail": row["creation_thumbnail"],
                    "creation_title": row["creation_title"],
                    "keyword": row["keyword"],
                    "number_of_reviews": row["number_of_reviews"],
                    "seller": {
                        "seller_email": row["seller_email"],
                        "seller_id": row["seller_id"],
                        "seller_name": row["seller_name"],
                        "seller_profile_photo": row["seller_profile_photo"]
                    },
                    "total_copy_sell": row["total_copy_sell"]
                })

            return jsonify({
                "data": result_list,
                "limit": limit,
                "offset": offset,
                "query": user_query
            }), 200

        except Exception as e:
            return jsonify({"message": f"Server error: {str(e)}"}), 500
