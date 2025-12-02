import os
import uuid
from datetime import datetime
from flask import Blueprint, request, make_response, send_file, jsonify
from werkzeug.security import generate_password_hash
import random
import string
import time

from model.user import UserModel
from app.utils.decorators import safe_route, require_user

user_bp = Blueprint('user', __name__, url_prefix='/users')


def generate_reference_code(length=6):
    """Generate a unique reference code"""
    timestamp = int(time.time())
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{timestamp}{random_part}"


# =======================
# LIST & CREATE OPERATIONS
# =======================

@user_bp.route("/")
@safe_route
def getUsers():
    """Get all users"""
    user_model = UserModel()
    result = user_model.get_all_users()
    user_model.close()
    
    if result['success']:
        if result['data']:
            res = make_response({"data": result['data']}, 200)
        else:
            res = make_response({"message": "No users found"}, 204)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


@user_bp.route("/paginated", methods=['GET'])
@safe_route
def getUsersWithPagination():
    """Get users with pagination. Query params: limit, page"""
    limit = request.args.get('limit', 10, type=int)
    page = request.args.get('page', 1, type=int)
    offset = (limit * page) - limit
    
    user_model = UserModel()
    result = user_model.get_users_paginated(limit, offset)
    user_model.close()
    
    if result['success']:
        if result['data']:
            res = make_response({"data": result['data']}, 200)
        else:
            res = make_response({"message": "Data not found"}, 204)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


@user_bp.route("/create", methods=["POST"])
@safe_route
def addUser():
    """Add a new user"""
    data = request.get_json()
    # Normalize phone: accept either combined `user_contact` or separate `country_code` and `phone_number`
    country_code = data.get('country_code')
    phone_number = data.get('phone_number')
    if country_code and phone_number:
        # ensure there is a leading plus
        contact = f"+{country_code.lstrip('+')}{phone_number}"
    else:
        contact = data.get('user_contact')

    # Hash the password before storing
    try:
        hashed_password = generate_password_hash(data['user_password'], method='pbkdf2:sha256')
    except KeyError:
        return make_response({"error": "user_password is required"}, 400)
    except Exception as e:
        return make_response({"error": f"Password hashing error: {str(e)}"}, 500)

    user_model = UserModel()
    result = user_model.create_user(
        data.get('user_name'),
        hashed_password,
        country_code,
        phone_number,
        data.get('role'),
        generate_reference_code()
    )
    user_model.close()
    
    if result['success']:
        res = make_response({"message": "User added successfully", "user_id": result['user_id']}, 200)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


# =======================
# READ OPERATIONS
# =======================

@user_bp.route("/profile")
@safe_route
@require_user
def getUserById():
    """Get current user by token"""
    user_id = getattr(request, 'user_id', None)
    
    user_model = UserModel()
    result = user_model.get_user_by_id(user_id)
    user_model.close()
    
    if result['success']:
        if result['data']:
            res = make_response({"data": result['data']}, 200)
        else:
            res = make_response({"error": "No user found"}, 204)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


@user_bp.route("/checkNumber", methods=["POST"])
@safe_route
def checkNumber():
    """Check if phone number already exists"""
    data = request.get_json()
    # Accept separate country_code + phone_number or combined user_contact
    country_code = data.get('country_code')
    phone_number = data.get('phone_number')
    if country_code and phone_number:
        contact = f"+{country_code.lstrip('+')}{phone_number}"
    else:
        contact = data.get('user_contact')

    user_model = UserModel()
    result = user_model.check_user_contact_exists(contact)
    user_model.close()
    
    if result['success']:
        res = make_response({"userExist": result['exists']}, 200)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


# =======================
# UPDATE OPERATIONS
# =======================

@user_bp.route("/update-user", methods=["PATCH"])
@safe_route
@require_user
def updateUser():
    """Update current user profile with optional file upload"""
    user_id = getattr(request, 'user_id', None)
    data = dict(request.form)
    files = request.files
    
    # Handle profile photo upload
    if 'profile_photo' in files:
        file = files['profile_photo']
        if file.filename:
            base_path = 'app/uploads/profilePick'
            os.makedirs(base_path, exist_ok=True)
            unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            file_path = os.path.join(base_path, unique_filename)
            file.save(file_path)
            data['profile_photo'] = file_path
    
    user_model = UserModel()
    result = user_model.update_user(user_id, data)
    user_model.close()
    
    if result['success']:
        if result['rowcount'] > 0:
            res = make_response({"message": "User updated successfully", "updated_data": data}, 200)
        else:
            res = make_response({"message": "Nothing to update"}, 204)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


@user_bp.route("/update-basic", methods=["PUT"])
@safe_route
def updateUserBasic():
    """Update user basic info"""
    data = dict(request.form)
    
    if not data:
        return make_response({"error": "No data provided"}, 400)
    
    user_id = data.get('user_id')
    if not user_id:
        return make_response({"error": "user_id is required"}, 400)
    
    # Remove user_id from update data
    update_data = {k: v for k, v in data.items() if k != 'user_id'}
    
    user_model = UserModel()
    result = user_model.update_user(user_id, update_data)
    user_model.close()
    
    if result['success']:
        if result['rowcount'] > 0:
            res = make_response({"message": "User updated successfully"}, 200)
        else:
            res = make_response({"message": "Nothing to update"}, 204)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


# =======================
# DELETE OPERATIONS
# =======================

@user_bp.route("/delete/<user_id>", methods=["DELETE"])
@safe_route
@require_user
def deleteUser(user_id):
    """Delete a user"""
    current_user_id = getattr(request, 'user_id', None)
    
    # Ensure user can only delete themselves
    if str(current_user_id) != str(user_id):
        return make_response({"error": "Unauthorized: can only delete your own account"}, 403)
    
    user_model = UserModel()
    result = user_model.delete_user(user_id)
    user_model.close()
    
    if result['success']:
        if result['rowcount'] > 0:
            res = make_response({"message": "User deleted successfully"}, 200)
        else:
            res = make_response({"message": "Nothing to delete"}, 204)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


# =======================
# FILE OPERATIONS
# =======================

@user_bp.route("/upload-avatar", methods=["PUT", "POST"])
@safe_route
@require_user
def uploadUserAvatar():
    """Upload user avatar/profile picture"""
    if 'avatar' not in request.files:
        return make_response({"error": "No avatar file provided"}, 400)
    
    file = request.files['avatar']
    user_id = getattr(request, 'user_id', None)
    
    if not file.filename:
        return make_response({"error": "Empty filename"}, 400)
    
    # Generate unique filename
    uniquename = str(datetime.now().timestamp()).replace(".", "")
    fileNameSplit = file.filename.split('.')
    ext = fileNameSplit[-1] if len(fileNameSplit) > 1 else 'bin'
    
    # Ensure directory exists
    upload_dir = 'app/uploads/profilePick'
    os.makedirs(upload_dir, exist_ok=True)
    
    finalPath = f"{upload_dir}/{user_id}-{uniquename}.{ext}"
    file.save(finalPath)
    
    user_model = UserModel()
    result = user_model.update_profile_photo(user_id, finalPath)
    user_model.close()
    
    if result['success']:
        res = make_response({"message": "File uploaded successfully"}, 200)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


@user_bp.route("/avatar/<filename>", methods=["GET"])
@safe_route
def getAvatar(filename):
    """Serve user avatar from uploads directory"""
    try:
        file_path = f"app/uploads/profilePick/{filename}"
        return send_file(file_path)
    except FileNotFoundError:
        return make_response({"error": "File not found"}, 404)


@user_bp.route("/file/<filename>", methods=["GET"])
@safe_route
def getFile(filename):
    """Serve any file from uploads directory"""
    try:
        file_path = f"app/uploads/{filename}"
        return send_file(file_path)
    except FileNotFoundError:
        return make_response({"error": "File not found"}, 404)
