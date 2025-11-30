import pymysql
from model.db import get_db_connection


class CreationModel:
    """Creation data access model"""
    
    def __init__(self):
        self.con = get_db_connection()
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)
        self.con.autocommit = True

    def create_creation(self, user_id, creation_title, creation_description, creation_price, 
                       creation_thumbnail, creation_file, category_id, keyword, 
                       creation_other_images, total_copy_sell, status, youtube_link):
        """Insert a new creation"""
        query = """
        INSERT INTO creations (creation_title, creation_description, creation_price, 
                              creation_thumbnail, creation_file, category_id, keyword, 
                              creation_other_images, total_copy_sell, user_id, status, youtube_link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cur.execute(query, (
                creation_title, creation_description, creation_price, creation_thumbnail,
                creation_file, category_id, keyword, creation_other_images, 
                total_copy_sell, user_id, status, youtube_link if youtube_link else None
            ))
            self.con.commit()
            return {"success": True, "message": "Creation added successfully"}
        except pymysql.MySQLError as e:
            self.con.rollback()
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def get_user_listed_creations(self, user_id):
        """Fetch all creations listed by a user"""
        query = "SELECT * FROM creations WHERE user_id = %s"
        try:
            self.cur.execute(query, (user_id,))
            results = self.cur.fetchall()
            return {"success": True, "data": results}
        except pymysql.MySQLError as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def get_purchased_creations(self, user_id):
        """Fetch all creations purchased by a user"""
        query = """
        SELECT 
            c.creation_id,
            c.creation_title,
            c.creation_description,
            c.creation_thumbnail,
            c.creation_file,
            od.price AS purchased_price,  
            o.order_id,
            o.order_date,
            IFNULL(AVG(r.rating), 0) AS avg_rating

        FROM users u
        JOIN orders o ON u.user_id = o.user_id
        JOIN order_details od ON o.order_id = od.order_id
        JOIN creations c ON od.creation_id = c.creation_id
        JOIN users seller ON c.user_id = seller.user_id
        LEFT JOIN ratings r ON c.creation_id = r.creation_id

        WHERE u.user_id = %s
        GROUP BY c.creation_id, od.price, od.gst_amount, od.platform_fee, o.order_id
        """
        try:
            self.cur.execute(query, (user_id,))
            results = self.cur.fetchall()
            return {"success": True, "data": results}
        except pymysql.MySQLError as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def get_purchased_creation_details(self, user_id, creation_id):
        """Fetch details of a purchased creation"""
        query = """
        SELECT
            c.creation_id,
            c.creation_title,
            c.creation_description,
            c.creation_price,
            c.creation_thumbnail,
            c.creation_file,
            c.category_id,
            c.creation_other_images,
            c.status,
            c.createtime,
            c.youtube_link,
            c.last_updated,

            od.price AS purchased_price,
            od.gst_amount,
            od.platform_fee,
            o.order_id,
            o.order_date,

            seller.user_id AS seller_id,
            seller.user_name AS seller_name,
            seller.user_email AS seller_email,
            seller.profile_photo AS seller_profile,

            IFNULL(r.avg_rating, 0) AS avg_rating,
            IFNULL(r.total_reviews, 0) AS total_reviews,
            IFNULL(l.total_likes, 0) AS total_likes,
            IFNULL(ul.is_liked, 0) AS is_liked_by_user,
            IFNULL(cs.total_copy_sold, 0) AS total_copy_sold,

            g.gst_percentage,
            pf.fee_percentage AS platform_fee_percentage

        FROM users u
        JOIN orders o ON u.user_id = o.user_id
        JOIN order_details od ON o.order_id = od.order_id
        JOIN creations c ON od.creation_id = c.creation_id
        JOIN users seller ON c.user_id = seller.user_id

        LEFT JOIN categories cat ON c.category_id = cat.category_id
        LEFT JOIN gst_rates g ON cat.gst = g.gst_id
        LEFT JOIN platform_fees pf ON cat.platform_fee_id = pf.fee_id

        LEFT JOIN (
            SELECT 
                creation_id,
                AVG(rating) AS avg_rating,
                COUNT(*) AS total_reviews
            FROM ratings
            GROUP BY creation_id
        ) r ON c.creation_id = r.creation_id

        LEFT JOIN (
            SELECT 
                creation_id,
                COUNT(*) AS total_likes
            FROM creation_likes
            GROUP BY creation_id
        ) l ON c.creation_id = l.creation_id

        LEFT JOIN (
            SELECT 
                creation_id,
                1 AS is_liked
            FROM creation_likes
            WHERE user_id = %s
        ) ul ON c.creation_id = ul.creation_id

        LEFT JOIN (
            SELECT 
                creation_id,
                COUNT(*) AS total_copy_sold
            FROM order_details
            GROUP BY creation_id
        ) cs ON c.creation_id = cs.creation_id

        WHERE u.user_id = %s AND c.creation_id = %s
        LIMIT 1
        """
        try:
            self.cur.execute(query, (user_id, user_id, creation_id))
            result = self.cur.fetchone()
            return {"success": True, "data": result}
        except pymysql.MySQLError as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def get_recently_added_creations(self, page_no, per_page, current_user_id):
        """Fetch recently added creations with pagination"""
        offset = (page_no - 1) * per_page
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
        LIMIT %s OFFSET %s
        """
        try:
            self.cur.execute(query, (current_user_id, current_user_id, per_page, offset))
            results = self.cur.fetchall()
            return {"success": True, "data": results}
        except pymysql.MySQLError as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def get_trending_creations(self, page_no, per_page, current_user_id):
        """Fetch trending creations with pagination"""
        offset = (page_no - 1) * per_page
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
            c.total_copy_sell DESC
        LIMIT %s OFFSET %s
        """
        try:
            self.cur.execute(query, (current_user_id, current_user_id, per_page, offset))
            results = self.cur.fetchall()
            return {"success": True, "data": results}
        except pymysql.MySQLError as e:
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
