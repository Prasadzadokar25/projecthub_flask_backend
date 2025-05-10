
from flask import make_response, request

from app.database_connection.db_connection import get_db_connection
from model.creation_model import CreationModel


class UserListedCreationController:
    def listCreationModel(self, data, filePaths):
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = """
            INSERT INTO creations (creation_title, creation_description, creation_price, creation_thumbnail, creation_file, category_id, keyword, creation_other_images, total_copy_sell, user_id, status, youtube_link)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
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
                data.get('status', 'underreview'),
                data['youtube_link'] if data['youtube_link'] != "" else None
            ))
            connection.commit()
            response = make_response({"message": "Creation added successfully"}, 200)
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response
        except Exception as e:
            if connection:
                connection.rollback()
            response = make_response({"error": str(e)}, 500)
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response
        finally:
            if connection:
                connection.close()

    def getUserListedCreations(self, user_id):
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = "SELECT * FROM creations WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchall()
            response = make_response({"data": result}, 200)
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response
        except Exception as e:
            if connection:
                connection.rollback()
            response = make_response({"error": str(e)}, 500)
            response.headers['Access-Control-Allow-Origin'] = "*"
            return response
        finally:
            if connection:
                connection.close()