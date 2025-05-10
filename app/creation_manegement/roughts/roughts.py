
import os
import uuid
from flask import Blueprint, request
from app.creation_manegement.controller.purchesed_creation_controller import PurchasedCreationController
from app.creation_manegement.controller.user_listed_creation_controller import UserListedCreationController


creation_bp = Blueprint('creation', __name__, url_prefix='/creation')

@creation_bp.route("/userListedCreations/<user_id>",methods=['GET'])
def userListedCreations(user_id):
    obj = UserListedCreationController()
    return obj.getUserListedCreations(user_id)

@creation_bp.route("/listCreation",methods=['POST'])
def listCreation():
    if 'creation_thumbnail' not in request.files or 'creation_file' not in request.files:
        return "No file part", 400
    obj = UserListedCreationController()
    base_path_scorcFile = 'app/uploads/creation/sourcefile/'
    base_path_thumbnail = 'app/uploads/creation/thumbnail/'
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


@creation_bp.route('/purchesed', methods=['GET'])
def get_purchesed_creations():
        user_id = request.args.get('user_id')
        purchasedCreationController = PurchasedCreationController()
        return purchasedCreationController.get_purchased_creations(user_id)

@creation_bp.route('/purchesed-details', methods=['GET'])
def get_purchesed_creation_details():
        user_id = request.args.get('user_id')
        creation_id = request.args.get('creation_id')
        purchasedCreationController = PurchasedCreationController()
        return purchasedCreationController.get_purchased_creation_details(user_id,creation_id)

