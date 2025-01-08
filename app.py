from flask import Flask
from model.user_model import UserModel
from model.login_model import LoginModel
from model.creation_model import CreationModel
from flask import request,send_file
from datetime import datetime
import uuid
import os

app = Flask(__name__)

@app.route("/")
def welcome():
    return "hello word"

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
    obj = CreationModel()
    base_path_scorcFile = 'uploads/creation/sourcefile/'
    base_path_thumbnail = 'uploads/creation/thumbnail/'

    data = request.form
    files = request.files
    creation_file = files['creation_file']
    creation_thumbnail = files['creation_thumbnail']
        
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
    


# Import the controllers to register routes
import controller.user_controller
import controller.creation_controller

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
