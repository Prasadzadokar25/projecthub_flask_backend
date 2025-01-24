import pymysql
import json
from pymysql.cursors import DictCursor
from flask import make_response

class CreationModel:
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
            
    def listCreationModel(self,data,filePaths):
        query = """
        INSERT INTO creations (creation_title, creation_description, creation_price, creation_thumbnail, creation_file, category_id, keyword, creation_other_images, total_copy_sell, user_id, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        self.cur.execute(query, (
            data['creation_title'],
            data['creation_description'],
            data['creation_price'],
            filePaths['thumbnail'],
            filePaths['souce_file'],
            data['category_id'],
            data['keyword'],
            data.get('creation_other_images', None),
            data.get('total_copy_sell', 0),
            data['user_id'],
            data.get('status', 'underreview')
        ))
        self.con.commit()
        responce = make_response({"message": "Creation added successfully"}, 200)
        responce.headers['Access-Control-Allow-Origin'] = "*"
        return responce
    
    def getCreationDetails(self, creation_id):
        query = """
        SELECT 
            c.creation_id, 
            c.creation_title, 
            c.creation_description, 
            c.creation_price, 
            c.creation_thumbnail, 
            c.creation_file, 
            cat.category_name, 
            cat.category_description, 
            COALESCE(AVG(r.rating), 0) AS average_rating
        FROM 
            creations c
        INNER JOIN 
            categories cat ON c.category_id = cat.category_id
        LEFT JOIN 
            ratings r ON c.creation_id = r.creation_id
        WHERE 
            c.creation_id = %s
        GROUP BY 
            c.creation_id, c.creation_title, c.creation_description, c.creation_price, 
            c.creation_thumbnail, c.creation_file, cat.category_name, cat.category_description
        """
        
        self.cur.execute(query, (creation_id,))
        creation_details = self.cur.fetchone()
        
        if creation_details:
            result = {
                "creation_id": creation_details[0],
                "creation_title": creation_details[1],
                "creation_description": creation_details[2],
                "creation_price": creation_details[3],
                "creation_thumbnail": creation_details[4],
                "creation_file": creation_details[5],
                "category_name": creation_details[6],
                "category_description": creation_details[7],
                "average_rating": creation_details[8]
            }
            return make_response(result, 200)
        else:
            return make_response({"message": "Creation not found"}, 404)


    def getCreationsModel(self,pageNo,perPage):
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
            c.keyword,
            c.createtime,

            c.creation_other_images,
            c.total_copy_sell,
            u.user_id AS seller_id,
            u.user_name AS seller_name,
            u.user_email AS seller_email,
            u.profile_photo AS seller_profile_photo,
            COALESCE(AVG(r.rating), 0) AS average_rating,
            COUNT(r.rating_id) AS number_of_reviews
        FROM 
            creations c
        JOIN 
            users u ON c.user_id = u.user_id
        LEFT JOIN 
            ratings r ON c.creation_id = r.creation_id
        GROUP BY 
            c.creation_id, u.user_id
        LIMIT %s OFFSET %s;
        """

        self.cur.execute(query, (perPage, offset))
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
                "average_rating": result["average_rating"],
                "number_of_reviews": result["number_of_reviews"],
                "createtime": result["createtime"],

                "seller":seller_data
            }
            
            creations.append(creation_data)
        responce = make_response({"creations": creations, "page": pageNo, "limit": perPage}, 200)
        responce.headers['Access-Control-Allow-Origin'] = "*"

        return responce
        
    def getRecentlyAddedCreations(self,pageNo,perPage):
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
            COALESCE(AVG(r.rating), 0) AS average_rating,
            COUNT(r.rating_id) AS number_of_reviews
        FROM 
            creations c
        JOIN 
            users u ON c.user_id = u.user_id
        LEFT JOIN 
            ratings r ON c.creation_id = r.creation_id
        GROUP BY 
            c.creation_id, u.user_id
        order by (createtime) desc
        LIMIT %s OFFSET %s;
        """

        self.cur.execute(query, (perPage, offset))
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
                "average_rating": result["average_rating"],
                "number_of_reviews": result["number_of_reviews"],
                "createtime": result["createtime"],
                "seller":seller_data
            }
            
            creations.append(creation_data)
        responce = make_response({"creations": creations, "page": pageNo, "limit": perPage}, 200)
        responce.headers['Access-Control-Allow-Origin'] = "*"

        return responce
    
    def getTrendingCreations(self,pageNo,perPage):
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
            COALESCE(AVG(r.rating), 0) AS average_rating,
            COUNT(r.rating_id) AS number_of_reviews
        FROM 
            creations c
        JOIN 
            users u ON c.user_id = u.user_id
        LEFT JOIN 
            ratings r ON c.creation_id = r.creation_id
        GROUP BY 
            c.creation_id, u.user_id
        order by (total_copy_sell) desc
        LIMIT %s OFFSET %s;
        """

        self.cur.execute(query, (perPage, offset))
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
                "average_rating": result["average_rating"],
                "number_of_reviews": result["number_of_reviews"],
                "createtime": result["createtime"],
                "seller":seller_data
            }
            
            creations.append(creation_data)
        responce = make_response({"creations": creations, "page": pageNo, "limit": perPage}, 200)
        responce.headers['Access-Control-Allow-Origin'] = "*"

        return responce
        
    def getUserListedCreations(self,user_id):
        query = f"select * from Creations where user_id = {user_id}"
        self.cur.execute(query)
        result = self.cur.fetchall()
        responce = make_response({"data": result}, 200)
        responce.headers['Access-Control-Allow-Origin'] = "*"
        return responce

        
        
            
    def getPurchedCreations(self,pageNo,perPage,uid):
        print("pppppppppppppppppppppppp")

        offset = (pageNo - 1) * perPage
        query = """
        SELECT 
            JSON_OBJECT(
                'order_id', o.order_id,
                'order_date', o.order_date,
                'purchase_price', od.price,
                'creation', JSON_OBJECT(
                    'creation_id', c.creation_id,
                    'creation_title', c.creation_title,
                    'creation_description', c.creation_description,
                    'creation_thumbnail', c.creation_thumbnail,
                    'creation_file', c.creation_file,
                    'category_id', c.category_id,
                    'creation_other_images', c.creation_other_images,
                    'total_copy_sell', c.total_copy_sell
                )
            ) AS creation_details
        FROM 
            orders o
        JOIN 
            order_details od ON o.order_id = od.order_id
        JOIN 
            creations c ON od.creation_id = c.creation_id
        WHERE 
            o.user_id = %s
        LIMIT %s OFFSET %s;
        """

        self.cur.execute(query, (uid,perPage,offset))
        result = self.cur.fetchall()
        responce = make_response({"data": result, "page": pageNo, "limit": perPage}, 200)
        responce.headers['Access-Control-Allow-Origin'] = "*"
        try:
            pass
            
        except:
            responce = make_response({"error": "Internal server error"}, 400)
            responce.headers['Access-Control-Allow-Origin'] = "*"

        return responce
        
    def addCreationInUserCard(self,data):
        print( data['userId'],
                data['creationId'],)
        try:
            query = """
                INSERT INTO carditems (user_id, creation_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE added_on = CURRENT_TIMESTAMP;

            """

            # Executing the query with data passed from the request
            self.cur.execute(query, (
                data['userId'],
                data['creationId'],
            ))

            # Committing the transaction
            self.con.commit()

            # Creating a response to send back to the client
            response = make_response({"message": "Creation added to card successfully"}, 200)
            response.headers['Access-Control-Allow-Origin'] = "*"  # Allowing CORS

            return response

        except Exception as e:
            # Handling errors and rolling back the transaction
            self.con.rollback()
            response = make_response({"message": f"Error: {str(e)}"}, 500)
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response
        
    def getInCardCreation(self,uid):
        try:
            query = """
                SELECT 
    JSON_OBJECT(
        'carditem_id', ci.carditem_id,
        'added_on', ci.added_on,
        'creation', JSON_OBJECT(
            'creation_id', c.creation_id,
            'creation_title', c.creation_title,
            'creation_description', c.creation_description,
            'creation_price', c.creation_price,
            'creation_thumbnail', c.creation_thumbnail,
            'creation_file', c.creation_file,
            'keyword', c.keyword,
            'creation_other_images', c.creation_other_images,
            'total_copy_sell', c.total_copy_sell,
            'gst_percentage', g.gst_percentage,
            'platform_fee_percentage', p.fee_percentage,
            'average_rating',ROUND(IFNULL(
            (SELECT AVG(r.rating) 
             FROM ratings r 
             WHERE r.creation_id = c.creation_id), 0
            ), 3), 
             'seller', JSON_OBJECT(
            'seller_id', s.user_id,
            'seller_name', s.user_name,
            'seller_contact', s.user_contact,
            'seller_email', s.user_email
        )
        )
       
    ) AS card_item_details
FROM 
    carditems ci
JOIN 
    creations c ON ci.creation_id = c.creation_id
JOIN 
    categories cat ON c.category_id = cat.category_id
JOIN 
    gst_rates g ON cat.gst = g.gst_id
JOIN 
    platform_fees p ON cat.platform_fee_id = p.fee_id
JOIN 
    users u ON ci.user_id = u.user_id
JOIN 
    users s ON c.user_id = s.user_id
WHERE 
    ci.user_id = %s AND ci.status = 1;

            """

            # Executing the query with data passed from the request
            self.cur.execute(query, (uid))
            
            result = self.cur.fetchall()

            # Creating a response to send back to the client
            response = make_response({"data": result}, 200)
            response.headers['Access-Control-Allow-Origin'] = "*"  # Allowing CORS

            return response

        except Exception as e:
            # Handling errors and rolling back the transaction
            self.con.rollback()
            response = make_response({"message": f"Error: {str(e)}"}, 500)
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response  
           
    def removeFromCart(self, data):
        
        uid = data['user_id']
        carditem_id = data['carditem_id']
        try:
            # Query to update the status of the item to 0 (removed from the cart)
            query = """
                UPDATE carditems
                SET status = 0
                WHERE user_id = %s AND carditem_id = %s AND status = 1;
            """
            
            # Execute the query with the provided user_id and carditem_id
            self.cur.execute(query, (uid, carditem_id))
            
            # Commit the transaction to save the changes
            self.con.commit()
            
            # Check if any row was affected (to confirm the item was in the cart)
            if self.cur.rowcount > 0:
                response = make_response({"message": "Item removed successfully."}, 200)
            else:
                response = make_response({"message": "Item not found in the cart."}, 404)

            response.headers['Access-Control-Allow-Origin'] = "*"  # Allowing CORS
            return response

        except Exception as e:
            # Rollback the transaction in case of an error
            self.con.rollback()
            response = make_response({"message": f"Error: {str(e)}"}, 500)
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response
