import pymysql
import json
from pymysql.cursors import DictCursor
from flask import jsonify, make_response
import os
import uuid


UPLOAD_FOLDER = 'static/uploads/'  # Ensure this folder exists
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AdvertisementModel:
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
            
    
            
    def add_advertisement(self,request):
        try:
            data = request.form  # For form data
            file = request.files.get('ad_image')  # For file

            # Extract text fields
            ad_title = data.get('ad_title')
            ad_description = data.get('ad_description')
            ad_website = data.get('ad_website')
            ad_start_date = data.get('ad_start_date')
            ad_end_date = data.get('ad_end_date')
            ad_duration = data.get('ad_duration')
            target_locations = json.dumps(json.loads(data.get('target_locations')))
            target_categories = json.dumps(json.loads(data.get('target_categories')))
            is_creation = data.get('is_creation', 1)
            is_active = data.get('is_active', 1)
            payment_id = data.get('payment_id')
            ad_owner_id = data.get('ad_owner_id')
            platform_target = json.dumps(json.loads(data.get('platform_target', '["android", "web"]')))
            priority_level = data.get('priority_level', 1)
            ad_type = data.get('ad_type', 'banner')
            target_impression_count = data.get('target_impression_count', 0)

            # Handle image file
            if not file or not allowed_file(file.filename):
                return make_response({'error': 'Invalid or missing image file'}, 400)
            
            base_path_scorcFile = 'uploads/advertisements/ad_images/'
            unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]

            image_path = base_path_scorcFile + unique_filename
            file.save(base_path_scorcFile+unique_filename)

            file.save(image_path)
            ad_image = image_path  # Save this to DB

            # Validate required fields
            required = [ad_title, ad_description, ad_start_date, ad_end_date, ad_duration, target_locations, target_categories]
            print(required)
            if not all(required):
                
                return make_response({'error': 'Missing required fields'}, 400)

            query = """
                INSERT INTO advertisements (
                    is_creation, ad_title, ad_description, ad_website, ad_image,
                    ad_start_date, ad_end_date, ad_duration, target_locations,
                    target_categories, is_active, payment_id, ad_owner_id,
                    platform_target, priority_level, ad_type, target_impression_count
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
            """

            values = (
                is_creation, ad_title, ad_description, ad_website, ad_image,
                ad_start_date, ad_end_date, ad_duration, target_locations,
                target_categories, is_active, payment_id, ad_owner_id,
                platform_target, priority_level, ad_type, target_impression_count
            )

            with self.con.cursor() as cursor:
                cursor.execute(query, values)
                self.con.commit()

            return jsonify({'message': 'Advertisement added successfully'}), 201

        except pymysql.MySQLError as err:
            print(f"MySQL Error: {err}")
            return jsonify({'error': str(err)}), 500
        except Exception as e:
            print(f"General Error: {e}")
            return jsonify({'error': str(e)}), 500

    def get_advertisements_by_location(self, user_id, location):
        print("location", location)
        print("user_id", user_id)
        try:
            query = """
                SELECT ad_description, ad_duration, ad_id, ad_image, ad_owner_id,
                    ad_title, ad_website, is_creation, priority_level
                FROM advertisements
                WHERE JSON_SEARCH(LOWER(target_locations), 'one', LOWER(%s)) IS NOT NULL
                AND is_active = 1
                AND ad_start_date <= CURDATE()
                AND ad_end_date >= CURDATE()
            """
            with self.con.cursor() as cursor:
                cursor.execute(query, (location,))
                advertisements = cursor.fetchall()

            if not advertisements:
                return jsonify({'message': 'No advertisements found for the specified location'}), 404

            return jsonify({'advertisements': advertisements}), 200

        except pymysql.MySQLError as err:
            print(f"MySQL Error: {err}")
            return jsonify({'error': str(err)}), 500
        except Exception as e:
            print(f"General Error: {e}")
            return jsonify({'error': str(e)}), 500
