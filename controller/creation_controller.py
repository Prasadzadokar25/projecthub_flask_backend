from app import app
from model.creation_model import CreationModel
from flask import request,send_file
from datetime import datetime
import uuid
import os

obj = CreationModel()


# @app.route("/listCreation",methods=['PUT'])
# def listCreation():
#     base_path_scorcFile = 'uploads/creation/sourcefile/'
#     base_path_thumbnail = 'uploads/creation/thumbnail/'

#     data = request.form
#     files = request.files
#     creation_file = files['creation_file']
#     creation_thumbnail = files['creation_thumbnail']
        
#     # Generate unique filenames
#     unique_filename = str(uuid.uuid4()) + os.path.splitext(creation_file.filename)[1]
#     unique_thumbnail = str(uuid.uuid4()) + os.path.splitext(creation_thumbnail.filename)[1]
    
#     creation_file.save(base_path_scorcFile+unique_filename)
#     creation_thumbnail.save(base_path_thumbnail+unique_thumbnail)
    
#     filePaths = {
#         "souce_file":base_path_scorcFile+unique_filename,
#         "thumbnail":base_path_thumbnail+unique_thumbnail
#     }
#     return obj.listCreationModel(data,filePaths)

@app.route("/getCreations",methods=['GET'])
def getCreations():
    return obj.getCreations()

# @app.route("/uploads/creation/thumbnail/<filename>",methods=['GET'])
# def getthumbnail(filename):
#     return send_file(f"uploads/creation/thumbnail/{filename}")

@app.route("/uploads/creation/sourcefile/<filename>",methods=['GET'])
def getsoucefile(filename):
    return send_file(f"uploads/creation/sourceFile/{filename}")