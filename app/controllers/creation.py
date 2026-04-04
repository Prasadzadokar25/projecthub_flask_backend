import os
import uuid
import mimetypes
from datetime import datetime
from flask import Blueprint, request, make_response, jsonify
from app.utils.decorators import safe_route, require_user
from model.creation import CreationModel

creation_bp = Blueprint('creation', __name__, url_prefix='/creations')


# =======================
# UTILITY FUNCTIONS
# =======================

def get_readable_file_size(size_in_bytes):
    """Convert bytes to human-readable format"""
    if size_in_bytes is None:
        return None
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} PB"


def get_readable_file_format(file_path):
    """Get readable file format"""
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


def structure_creation_data(row, include_seller=True):
    """Structure creation data for response"""
    creation_data = {
        "creation_id": row["creation_id"],
        "creation_title": row["creation_title"],
        "creation_description": row["creation_description"],
        "creation_price": str(row["creation_price"]) if "creation_price" in row else None,
        "creation_thumbnail": row["creation_thumbnail"],
        "creation_file": row["creation_file"],
        "category_id": row["category_id"],
        "keyword": row.get("keyword"),
        "creation_other_images": row.get("creation_other_images"),
        "total_copy_sell": row.get("total_copy_sell"),
        "avg_rating": row.get("avg_rating", 0),
        "number_of_reviews": row.get("number_of_reviews", 0),
        "createtime": row.get("createtime"),
        "total_likes": row.get("total_likes", 0),
        "isLikedByUser": bool(row.get("is_liked_by_user", 0)),
    }
    
    if include_seller and "seller_id" in row:
        creation_data["seller"] = {
            "seller_id": row["seller_id"],
            "seller_name": row["seller_name"],
            "seller_email": row["seller_email"],
            "seller_profile_photo": row["seller_profile_photo"]
        }
    
    return creation_data


# =======================
# USER LISTED CREATION ROUTES
# =======================

@creation_bp.route("/userListedCreations", methods=['GET'])
@safe_route
@require_user
def get_user_listed_creations():
    """Get all creations listed by the current user"""
    user_id = getattr(request, 'user_id', None)
    
    creation_model = CreationModel()
    result = creation_model.get_user_listed_creations(user_id)
    creation_model.close()
    
    if result['success']:
        res = make_response({"data": result['data']}, 200)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


@creation_bp.route("/listCreation", methods=['POST'])
@safe_route
@require_user
def list_creation():
    """Create and list a new creation with files"""
    if 'creation_thumbnail' not in request.files or 'creation_file' not in request.files:
        return make_response({"error": "No file part - both creation_thumbnail and creation_file are required"}, 400)
    
    user_id = getattr(request, 'user_id', None)
    data = dict(request.form)
    files = request.files
    
    creation_file = files['creation_file']
    creation_thumbnail = files['creation_thumbnail']
    
    if not creation_file.filename or not creation_thumbnail.filename:
        return make_response({"error": "Empty filename"}, 400)
    
    # Generate unique filenames
    base_path_source = 'app/uploads/creation/sourcefile/'
    base_path_thumbnail = 'app/uploads/creation/thumbnail/'
    
    os.makedirs(base_path_source, exist_ok=True)
    os.makedirs(base_path_thumbnail, exist_ok=True)
    
    unique_filename = str(uuid.uuid4()) + os.path.splitext(creation_file.filename)[1]
    unique_thumbnail = str(uuid.uuid4()) + os.path.splitext(creation_thumbnail.filename)[1]

    creation_file.save(base_path_source + unique_filename)
    creation_thumbnail.save(base_path_thumbnail + unique_thumbnail)

    file_paths = {
        "source_file": base_path_source + unique_filename,
        "thumbnail": base_path_thumbnail + unique_thumbnail
    }
    
    creation_model = CreationModel()
    result = creation_model.create_creation(
        user_id,
        data.get('creation_title'),
        data.get('creation_description'),
        data.get('creation_price'),
        file_paths['thumbnail'],
        file_paths['source_file'],
        data.get('category_id'),
        data.get('keyword'),
        data.get('creation_other_images'),
        data.get('total_copy_sell', 0),
        data.get('status', 'underreview'),
        data.get('youtube_link')
    )
    creation_model.close()
    
    if result['success']:
        res = make_response({"message": result['message']}, 201)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


# =======================
# PURCHASED CREATIONS ROUTES
# =======================

@creation_bp.route('/purchased', methods=['GET'])
@safe_route
@require_user
def get_purchased_creations():
    """Get all creations purchased by the current user"""
    user_id = getattr(request, 'user_id', None)
    
    creation_model = CreationModel()
    result = creation_model.get_purchased_creations(user_id)
    creation_model.close()
    
    if result['success']:
        structured_results = []
        for row in result['data']:
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
        res = make_response({"success": True, "data": structured_results}, 200)
    else:
        res = make_response({"success": False, "error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


@creation_bp.route('/purchased-details', methods=['GET'])
@safe_route
@require_user
def get_purchased_creation_details():
    """Get details of a specific purchased creation"""
    user_id = getattr(request, 'user_id', None)
    creation_id = request.args.get('creation_id')
    
    if not creation_id:
        return make_response({"error": "creation_id is required"}, 400)
    
    creation_model = CreationModel()
    result = creation_model.get_purchased_creation_details(user_id, creation_id)
    creation_model.close()
    
    if result['success']:
        if not result['data']:
            res = make_response({"success": False, "message": "No purchase found."}, 404)
        else:
            row = result['data']
            file_path = f"app/{row['creation_file']}"
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else None

            structured_result = {
                "purchased_price": str(row["purchased_price"]),
                "order_id": row["order_id"],
                "order_date": row["order_date"],
                "gst_amount": str(row["gst_amount"]),
                "platform_fee": str(row["platform_fee"]),
                "creation": {
                    "creation_id": row["creation_id"],
                    "creation_title": row["creation_title"],
                    "creation_description": row["creation_description"],
                    "creation_price": str(row["creation_price"]),
                    "gst_percentage": str(row["gst_percentage"]) if row["gst_percentage"] is not None else None,
                    "platform_fee_percentage": str(row["platform_fee_percentage"]) if row["platform_fee_percentage"] is not None else None,
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
                    "total_reviews": row["total_reviews"],
                    "total_likes": row["total_likes"],
                    "total_copy_sold": row["total_copy_sold"],
                    "is_liked_by_user": bool(row["is_liked_by_user"]),
                    "seller": {
                        "seller_id": row["seller_id"],
                        "seller_name": row["seller_name"],
                        "seller_email": row["seller_email"],
                        "seller_profile": row["seller_profile"],
                    }
                }
            }

            res = make_response({"success": True, "data": structured_result}, 200)
    else:
        res = make_response({"success": False, "error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


# =======================
# RECENTLY ADDED CREATIONS ROUTES
# =======================

@creation_bp.route('/homeScreenCreations', methods=['GET'])
@safe_route
def get_home_screen_creations():

    # Get current authenticated user ID from JWT
    current_user_id = getattr(request, "user_id", None)

    page = request.args.get('page', 1)
    perPage = request.args.get('perPage', 10)

    creation_model = CreationModel()
    result = creation_model.get_home_screen_creations(
        int(page),
        int(perPage),
        current_user_id
    )
    creation_model.close()

    if result['success']:
        creations = [structure_creation_data(row) for row in result['data']]
        res = make_response({
            "data": creations,
            "page": int(page),
            "limit": int(perPage),
            "current_user_id": current_user_id
        }, 200)
    else:
        res = make_response({"error": result['error']}, 500)

    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


# =======================
# TRENDING CREATIONS ROUTES
# =======================

@creation_bp.route('/trendingCreations/page/<page>/perPage/<perPage>', methods=['GET'])
@safe_route
def get_trending_creations(page, perPage):
    """Get trending creations with pagination"""
    current_user_id = getattr(request, 'user_id', None)
    
    creation_model = CreationModel()
    result = creation_model.get_trending_creations(int(page), int(perPage), current_user_id)
    creation_model.close()
    
    if result['success']:
        creations = [structure_creation_data(row) for row in result['data']]
        res = make_response({"creations": creations, "page": int(page), "limit": int(perPage)}, 200)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res
