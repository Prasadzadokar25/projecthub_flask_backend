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


    def getCreations(self):
        query = "select * from Creations"
        self.cur.execute(query)
        result = self.cur.fetchall()
        responce = make_response({"data": result}, 200)
        return responce

        
        
            
    