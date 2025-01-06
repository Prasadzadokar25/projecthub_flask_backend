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

    def getCreations(self):
        query = "select * from Creations"
        self.cur.execute(query)
        result = self.cur.fetchall()
        responce = make_response({"data": result}, 200)
        return responce

        
        
            
    