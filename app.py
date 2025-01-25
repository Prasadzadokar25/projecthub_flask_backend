from flask import Flask
from model.bank_account_model import BackAcountModel
from model.order_medel import OrderModel
from model.user_model import UserModel
from model.login_model import LoginModel
from model.creation_model import CreationModel
from flask import request,send_file
from datetime import datetime
import uuid
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def welcome():
    return "hello welcome to projecthub"

# user_controller.py

@app.route("/getUsers")
def getUsers():
    userobj = UserModel()
    return userobj.getUsersModel()

@app.route("/addUser",methods=["POST"])
def addUser():
    userobj = UserModel()
    data = request.get_json()
    return userobj.addUserModel(data)

@app.route("/getUser/<id>")
def getUserById(id):
    userobj = UserModel()
    return userobj.getUserByIdModel(id)

@app.route("/checkNumber",methods=["POST"])
def chechNumber():
    userobj = UserModel()
    data = request.get_json()
    return userobj.checkNumberModel(data['user_contact'])

@app.route("/checkLogin",methods=["POST"])
def checkLogin():
    userobj = LoginModel()
    data = request.get_json()
    return userobj.checkLoginDetailsModel(data)

# creation_controller.py

@app.route("/listCreation",methods=['POST'])
def listCreation():
    if 'creation_thumbnail' not in request.files or 'creation_file' not in request.files:
        return "No file part", 400
    obj = CreationModel()
    base_path_scorcFile = 'uploads/creation/sourcefile/'
    base_path_thumbnail = 'uploads/creation/thumbnail/'
    print("here1")
    data = request.form
    files = request.files
    creation_file = files['creation_file']
    creation_thumbnail = files['creation_thumbnail']
    print("here1")
    # Generate unique filenames
    unique_filename = str(uuid.uuid4()) + os.path.splitext(creation_file.filename)[1]
    unique_thumbnail = str(uuid.uuid4()) + os.path.splitext(creation_thumbnail.filename)[1]
    
    creation_file.save(base_path_scorcFile+unique_filename)
    creation_thumbnail.save(base_path_thumbnail+unique_thumbnail)
    
    filePaths = {
        "souce_file":base_path_scorcFile+unique_filename,
        "thumbnail":base_path_thumbnail+unique_thumbnail
    }
    return obj.listCreationModel(data,filePaths)

@app.route("/userListedCreations/<user_id>",methods=['GET'])
def userListedCreations(user_id):
    obj = CreationModel()
    return obj.getUserListedCreations(user_id)
    
@app.route('/creation/purched/page/<page>/perPage/<perPage>/uid/<uid>', methods=['GET'])
def purchedCreations(page,perPage,uid):
    obj = CreationModel()
    return obj.getPurchedCreations(int(page),int(perPage),uid)

@app.route('/creations/page/<page>/perPage/<perPage>/uid/<uid>', methods=['GET'])
def getCreations(page,perPage,uid):
    obj = CreationModel()
    return obj.getCreationsModel(int(page),int(perPage))

@app.route('/recentCreations/page/<page>/perPage/<perPage>/uid/<uid>', methods=['GET'])
def recentCreations(page,perPage,uid):
    obj = CreationModel()
    return obj.getRecentlyAddedCreations(int(page),int(perPage))

  
@app.route('/trendingCreations/page/<page>/perPage/<perPage>/uid/<uid>', methods=['GET'])
def trendingCreations(page,perPage,uid):
    obj = CreationModel()
    return obj.getTrendingCreations(int(page),int(perPage))
    
@app.route('/recomandedCreations/page/<page>/perPage/<perPage>/uid/<uid>', methods=['Post'])
def getRecomandedCreations(page,perPage,uid):
    obj = CreationModel()
    return obj.getTrendingCreations(int(page),int(perPage))

@app.route('/creation/card/add', methods=['POST'])
def addCreationInUserCard():
    data = request.get_json()
    obj = CreationModel()
    return obj.addCreationInUserCard(data)

@app.route('/creation/card/remove', methods=['POST'])
def removeFromCart():
    data = request.get_json()
    obj = CreationModel()
    return obj.removeFromCart(data)

@app.route('/creation/card/get/userid/<uid>', methods=['GET'])
def getInCardCreations(uid):
    obj = CreationModel()
    return obj.getInCardCreation(uid)
    
# bank_account_controller.py
@app.route('/add-bank-account', methods=['POST'])
def add_bank_account():
    data = request.get_json()
    obj =BackAcountModel()
    return obj.add_bank_account(data)

@app.route('/accounts/<int:user_id>', methods=['GET'])
def get_accounts_for_user(user_id):
    obj =BackAcountModel()
    return obj.get_accounts_for_user(user_id)

@app.route('/set-primary-account/<int:user_id>/<int:account_id>', methods=['PUT'])
def set_primary_account(user_id, account_id):
    obj = BackAcountModel()
    return obj.set_primary_account(user_id,account_id)

# payment_controller.py
@app.route('/create-order', methods=['POST'])
def create_order():
    obj = OrderModel()
    return obj.create_order()

    
# file_controller.py
@app.route("/uploads/creation/thumbnail/<filename>",methods=['GET'])
def getthumbnail(filename):
    return send_file(f"uploads/creation/thumbnail/{filename}")

@app.route('/uploads/creation/sourcefile/<filename>', methods=['GET'])
def download_file(filename):
    # Path to your ZIP file
    file_path = f'uploads/creation/sourcefile/{filename}'

    try:
        # Send the file to the client
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e), 404
    
# Import the controllers to register routes
import controller.user_controller
import controller.creation_controller

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
