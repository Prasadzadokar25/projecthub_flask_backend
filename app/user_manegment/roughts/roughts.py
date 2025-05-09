from flask import Blueprint, request
from app.user_manegment.controller.user_controller import UserController
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route("/get")
def getUsers():
    userobj = UserController()
    return userobj.getUsersModel()

@user_bp.route("/add",methods=["POST"])
def addUser():
    userobj = UserController()
    data = request.get_json()
    return userobj.addUserModel(data)

@user_bp.route('/update-user/<int:user_id>', methods=['PATCH'])
def updateUser(user_id):
    userobj = UserController()
    data = request.form
    files = request.files

    return userobj.update_user(user_id,data,files)

@user_bp.route("/getUser/<id>")
def getUserById(id):
    userobj = UserController()
    return userobj.getUserByIdModel(id)

@user_bp.route("/checkNumber",methods=["POST"])
def chechNumber():
    userobj = UserController()
    data = request.get_json()
    return userobj.checkNumberModel(data['user_contact'])

