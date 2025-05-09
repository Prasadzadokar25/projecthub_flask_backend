from run import app
from model.user_model import UserModel
from flask import request,send_file
from datetime import datetime
obj = UserModel()

# @app.route("/addUser",methods=["POST"])
# def addUser():
#     request.form
#     return obj.addUserModel(request.form)



# @app.route("/getUsers")
# def getUsers():
#     return obj.getUsersModel()

@app.route("/updateUser",methods=["PUT"])
def updateUser():
    return obj.updateUserModel(request.form)


@app.route("/deleteUser/<id>",methods=["DELETE"])
def deleteUser(id):
    return obj.deleteUserModel(id)

@app.route("/getUsers/limit/<limit>/page/<page>")
def getUsersWitPagination(limit,page):
    return obj.getUsersWitPaginationModel(limit,page)

@app.route("/users/<id>/upload/avatar",methods=['PUT'])
def uploadUserAvatar(id):
    file = request.files['avatar']
    # to save file with uniq name
    
    uniquename = str(datetime.now().timestamp()).replace(".","")
    fileNameSplit = file.filename.split(".")
    ext = fileNameSplit[len(fileNameSplit)-1]
    finalPath = f"upload/{id}-{uniquename}.{ext}"
    file.save(finalPath)
    return obj.uploadAvtarModel(id,finalPath)

@app.route("/getFile/<filename>")
def getfile(filename):
    return send_file(f"upload/{filename}")
    


    