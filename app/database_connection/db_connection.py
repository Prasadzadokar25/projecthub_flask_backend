import pymysql
from pymysql.cursors import DictCursor


def get_db_connection():
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
            con = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                cursorclass=DictCursor
            )
            con.autocommit = True
            print("connect succefuly")
            return con
        except pymysql.MySQLError as err:
            print(f"Failed to connect: {err}")
