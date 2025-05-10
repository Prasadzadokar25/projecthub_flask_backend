from flask import make_response
from app.database_connection.db_connection import get_db_connection


class RecentlyAddedCreationController:
    def getRecentlyAddedCreations(self, pageNo, perPage, current_user_id):
        connection = None
        self.cur = None
        try:
            connection = get_db_connection()
            self.cur = connection.cursor()
            offset = (pageNo - 1) * perPage
            query = """
            SELECT 
                c.creation_id,
                c.creation_title,
                c.creation_description,
                c.creation_price,
                c.creation_thumbnail,
                c.creation_file,
                c.category_id,
                c.createtime,
                c.keyword,
                c.creation_other_images,
                c.total_copy_sell,

                u.user_id AS seller_id,
                u.user_name AS seller_name,
                u.user_email AS seller_email,
                u.profile_photo AS seller_profile_photo,

                COALESCE(AVG(r.rating), 0) AS avg_rating,
                COUNT(r.rating_id) AS number_of_reviews,

                COUNT(DISTINCT cl.like_id) AS total_likes,
                MAX(CASE WHEN cl_user.user_id = %s THEN 1 ELSE 0 END) AS is_liked_by_user

            FROM 
                creations c
            JOIN 
                users u ON c.user_id = u.user_id
            LEFT JOIN 
                ratings r ON c.creation_id = r.creation_id
            LEFT JOIN 
                creation_likes cl ON c.creation_id = cl.creation_id
            LEFT JOIN 
                creation_likes cl_user ON c.creation_id = cl_user.creation_id AND cl_user.user_id = %s

            GROUP BY 
                c.creation_id, u.user_id
            ORDER BY 
                c.createtime DESC
            LIMIT %s OFFSET %s;
            """

            self.cur.execute(query, (current_user_id, current_user_id, perPage, offset))
            results = self.cur.fetchall()

            creations = []
            for result in results:
                seller_data = {
                    "seller_id": result["seller_id"],
                    "seller_name": result["seller_name"],
                    "seller_email": result["seller_email"],
                    "seller_profile_photo": result["seller_profile_photo"]
                }
                creation_data = {
                    "creation_id": result["creation_id"],
                    "creation_title": result["creation_title"],
                    "creation_description": result["creation_description"],
                    "creation_price": result["creation_price"],
                    "creation_thumbnail": result["creation_thumbnail"],
                    "creation_file": result["creation_file"],
                    "category_id": result["category_id"],
                    "keyword": result["keyword"],
                    "creation_other_images": result["creation_other_images"],
                    "total_copy_sell": result["total_copy_sell"],
                    "avg_rating": result["avg_rating"],
                    "number_of_reviews": result["number_of_reviews"],
                    "createtime": result["createtime"],
                    "total_likes": result["total_likes"],
                    "isLikedByUser": bool(result["is_liked_by_user"]),
                    "seller": seller_data
                }
                
                creations.append(creation_data)

            responce = make_response({"creations": creations, "page": pageNo, "limit": perPage}, 200)
            responce.headers['Access-Control-Allow-Origin'] = "*"

            return responce
        except Exception as e:
            print("Error in RecentlyAddedCreationController:", str(e))
            return make_response({"error": str(e)}, 500)
        finally:
            if self.cur:
                self.cur.close()
            if connection:
                connection.close()