import pymysql
import json
from pymysql.cursors import DictCursor
from flask import make_response
from flask import request, jsonify

class UserModel:
    
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
            
    def addUserModel(self,data):
        query = "INSERT INTO users ( user_name, user_password, user_description,user_contact,user_email,role,reference_code) VALUES (%s, %s, %s, %s,%s, %s, %s)"
        self.cur.execute(query, (data['user_name'], data['user_password'], data['user_description'],data['user_contact'],data['user_email'],data['role'],data['reference_code']))
        self.con.commit()
        res = make_response({"massage":"user added succefully"},200)
        res.headers['Access-Control-Allow-Origin']="*"
        return res

    
    def getUsersModel(self):
        qury = "select * from users"
        self.cur.execute(qury)
        result = self.cur.fetchall()
        #resultInStringFro = json.dumps(result)
        
        res = make_response({"data":result},200)
        res.headers['Access-Control-Allow-Origin']="*"
        return res
    
    # Pagination in rest api
    def getUsersWitPaginationModel(self,limit,page):
        
        limit = int(limit)
        page = int(page)
        start = (limit*page)-limit
        
        qury = f"select * from userinfo limit {start},{limit}"
        self.cur.execute(qury)
        result = self.cur.fetchall()
        #resultInStringFro = json.dumps(result)
        
        if len(result)>0:
            res = make_response({"data":result},200)
            res.headers['Access-Control-Allow-Origin']="*"
            return res
        else:
            res = make_response({"massage":"data not found"},204)
            res.headers['Access-Control-Allow-Origin']="*"
            return res
    
    
    def updateUserModel(self,data):
        query = f"update userInfo set username = '{data['name']}' where teacher_id={int(data['id'])}"
        self.cur.execute(query)
        self.con.commit()
        if  self.cur.rowcount>0:
            return "user updated succefuly"
        else:
            return "nottihing to update"
        
    def deleteUserModel(self,id):
        query = f"delete from userInfo where teacher_id={id}"
        self.cur.execute(query)
        self.con.commit()
        
        if  self.cur.rowcount>0:
            return "user deleted succefuly"
        else:
            return "nottihing to delete"
        
    def uploadAvtarModel(self,id,filePath):
        qry = f"Update userInfo Set avatr = '{filePath}' where teacher_id = {id}"
        self.cur.execute(qry)
        self.con.commit()

        if self.cur.rowcount>0:
            return {"maasage": "file uploaded succefuly"}
        else:
            return {"maasge":"file upload filled"}
        
        
    