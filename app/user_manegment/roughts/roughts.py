import os
from datetime import datetime
from flask import Blueprint, request, send_file
from app.user_manegment.controller.user_controller import UserController
from app.utils.decorators import safe_route, require_user

user_bp = Blueprint('user', __name__, url_prefix='/user')


# =======================
# LIST & CREATE OPERATIONS
# =======================

@user_bp.route("/get")
@safe_route
def getUsers():
    """Get all users"""
    userobj = UserController()
    return userobj.getUsersModel()


@user_bp.route("/get/paginated", methods=['GET'])
@safe_route
def getUsersWithPagination():
    """Get users with pagination. Query params: limit, page"""
    userobj = UserController()
    limit = request.args.get('limit', 10, type=int)
    page = request.args.get('page', 1, type=int)
    return userobj.getUsersWitPaginationModel(limit, page)


@user_bp.route("/add", methods=["POST"])
@safe_route
def addUser():
    """Add a new user"""
    userobj = UserController()
    data = request.get_json()
    return userobj.addUserModel(data)


# =======================
# READ OPERATIONS
# =======================

@user_bp.route("/getUser")
@safe_route
@require_user
def getUserById():
    """Get current user by token"""
    userobj = UserController()
    user_id = getattr(request, 'user_id', None)
    return userobj.getUserByIdModel(user_id)


@user_bp.route("/checkNumber", methods=["POST"])
@safe_route
def checkNumber():
    """Check if phone number already exists"""
    userobj = UserController()
    data = request.get_json()
    return userobj.checkNumberModel(data['user_contact'])


# =======================
# UPDATE OPERATIONS
# =======================

@user_bp.route("/update-user", methods=["PATCH"])
@safe_route
@require_user
def updateUser():
    """Update current user profile with optional file upload"""
    userobj = UserController()
    data = request.form
    files = request.files
    user_id = getattr(request, 'user_id', None)
    return userobj.update_user(user_id, data, files)


@user_bp.route("/update-basic", methods=["PUT"])
@safe_route
def updateUserBasic():
    """Update user basic info (legacy endpoint)"""
    userobj = UserController()
    return userobj.updateUserModel(request.form)


# =======================
# DELETE OPERATIONS
# =======================

@user_bp.route("/delete/<user_id>", methods=["DELETE"])
@safe_route
@require_user
def deleteUser(user_id):
    """Delete a user"""
    userobj = UserController()
    # Ensure user can only delete themselves or is admin
    current_user_id = getattr(request, 'user_id', None)
    if str(current_user_id) != str(user_id):
        return {"error": "Unauthorized: can only delete your own account"}, 403
    return userobj.deleteUserModel(user_id)


# =======================
# FILE OPERATIONS
# =======================

@user_bp.route("/upload-avatar", methods=["PUT", "POST"])
@safe_route
@require_user
def uploadUserAvatar():
    """Upload user avatar/profile picture"""
    if 'avatar' not in request.files:
        return {"error": "No avatar file provided"}, 400
    
    file = request.files['avatar']
    user_id = getattr(request, 'user_id', None)
    
    if not file.filename:
        return {"error": "Empty filename"}, 400
    
    # Generate unique filename
    uniquename = str(datetime.now().timestamp()).replace(".", "")
    fileNameSplit = file.filename.split('.')
    ext = fileNameSplit[len(fileNameSplit)-1] if len(fileNameSplit) > 1 else 'bin'
    
    # Ensure directory exists
    upload_dir = 'app/uploads/profilePick'
    os.makedirs(upload_dir, exist_ok=True)
    
    finalPath = f"{upload_dir}/{user_id}-{uniquename}.{ext}"
    file.save(finalPath)
    
    userobj = UserController()
    return userobj.uploadAvtarModel(user_id, finalPath)


@user_bp.route("/avatar/<filename>", methods=["GET"])
@safe_route
def getAvatar(filename):
    """Serve user avatar from uploads directory"""
    try:
        file_path = f"app/uploads/profilePick/{filename}"
        return send_file(file_path)
    except FileNotFoundError:
        return {"error": "File not found"}, 404


@user_bp.route("/file/<filename>", methods=["GET"])
@safe_route
def getFile(filename):
    """Serve any file from uploads directory (legacy endpoint)"""
    try:
        file_path = f"app/uploads/{filename}"
        return send_file(file_path)
    except FileNotFoundError:
        return {"error": "File not found"}, 404

