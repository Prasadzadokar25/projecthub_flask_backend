from flask import Flask
from model.user_model import UserModel
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
    print(request.form['user_name'])
    return userobj.addUserModel(request.form)

# Import the controllers to register routes
import controller.user_controller
import controller.creation_controller

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
