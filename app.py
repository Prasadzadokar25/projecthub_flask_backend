from flask import Flask
from model.user_model import UserModel
from model.login_model import LoginModel
from flask import request,send_file

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
    


# Import the controllers to register routes
import controller.user_controller
import controller.creation_controller

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
