import mimetypes
import os
from flask import  jsonify
from app.database_connection.db_connection import get_db_connection

class PurchasedCreationController:
    def get_purchased_creations(self,user_id):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
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

                cursor.execute(query, (user_id))
                results = cursor.fetchall()
                
                # Structure seller data inside a nested map
                structured_results = []
                for row in results:

                    structured_results.append({
                    
                        "purchased_price": str(row["purchased_price"]),
                        "order_id": row["order_id"],
                        "order_date": row["order_date"],
                        "creation_id": row["creation_id"],
                        "creation_title": row["creation_title"],
                        "creation_description": row["creation_description"],
                        "creation_thumbnail": row["creation_thumbnail"],
                        "creation_file": row["creation_file"],      
                    })

                return jsonify({"success": True, "data": structured_results})

        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
        
        finally:
            connection.close()
    
    def get_purchased_creation_details(self,user_id,creation_id):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
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

                        IFNULL(AVG(r.rating), 0) AS avg_rating

                    FROM users u
                    JOIN orders o ON u.user_id = o.user_id
                    JOIN order_details od ON o.order_id = od.order_id
                    JOIN creations c ON od.creation_id = c.creation_id
                    JOIN users seller ON c.user_id = seller.user_id
                    LEFT JOIN ratings r ON c.creation_id = r.creation_id

                    WHERE u.user_id = %s and c.creation_id = %s
                    GROUP BY c.creation_id, od.price, od.gst_amount, od.platform_fee, o.order_id
                """

                cursor.execute(query, (user_id,creation_id))
                results = cursor.fetchall()
                
                # Structure seller data inside a nested map
                structured_results = []
                for row in results:
                    file_path =f"app/{row["creation_file"]}"
                    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else None
                    file_format = mimetypes.guess_type(file_path)[0] if file_path else None

                    structured_results.append({
                    
                        "purchased_price": str(row["purchased_price"]),
                        "order_id": row["order_id"],
                        "order_date": row["order_date"],
                        "creation":{
                            "creation_id": row["creation_id"],
                            "creation_title": row["creation_title"],
                            "creation_description": row["creation_description"],
                            "creation_price": str(row["creation_price"]),
                            "gst_amount": str(row["gst_amount"]),
                            "platform_fee": str(row["platform_fee"]),
                            "creation_thumbnail": row["creation_thumbnail"],
                            "creation_file": row["creation_file"],
                            "file_format": get_readable_file_format(file_path),
                            "file_size": get_readable_file_size(file_size),
                            "category_id": row["category_id"],
                            "creation_other_images": row["creation_other_images"],
                            "createtime": row["createtime"],
                            "youtube_link": row["youtube_link"],
                            "last_updated": row["last_updated"],
                            "avg_rating": float(row["avg_rating"]),
                            "seller": {
                                "seller_id": row["seller_id"],
                                "seller_name": row["seller_name"],
                                "seller_email": row["seller_email"],
                                "seller_profile": row["seller_profile"],
                            }

                        },
                        
                    })

                return jsonify({"success": True, "data": structured_results})

        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
        
        finally:
            connection.close()


def get_readable_file_size(size_in_bytes):
    if size_in_bytes is None:
        return None
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} PB"  # If size is larger than TB, return in PB

import mimetypes
import os

def get_readable_file_format(file_path):
    if not file_path:
        return None

    # Try to guess from MIME type first
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        main_type, _, subtype = mime_type.partition('/')
        return subtype.upper() if subtype else mime_type.upper()

    # Fallback to file extension
    _, ext = os.path.splitext(file_path)
    if ext:
        return ext.replace('.', '').upper()

    return None
