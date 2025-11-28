
import os
import uuid
from flask import Blueprint, request
from app.creation_manegement.controller.purchesed_creation_controller import PurchasedCreationController
from app.creation_manegement.controller.recently_added_creation_controller import RecentlyAddedCreationController
from app.creation_manegement.controller.trending_creation_controller import TrendingCreationController
from app.creation_manegement.controller.user_listed_creation_controller import UserListedCreationController
from app.utils.decorators import safe_route, require_user


creation_bp = Blueprint('creation', __name__, url_prefix='/creation')


# user listed creation routes

@creation_bp.route("/userListedCreations",methods=['GET'])
@safe_route
@require_user
def userListedCreations():
    user_id = getattr(request, 'user_id', None)
    obj = UserListedCreationController()
    return obj.getUserListedCreations(user_id)

@creation_bp.route("/listCreation",methods=['POST'])
@safe_route
@require_user
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
    # ensure user identity is passed
    data = dict(data)
    data['user_id'] = getattr(request, 'user_id', None)
    return obj.listCreationModel(data,filePaths)


# purchesed creation routes
@creation_bp.route('/purchesed', methods=['GET'])
@safe_route
@require_user
def get_purchesed_creations():
    user_id = getattr(request, 'user_id', None)
    purchasedCreationController = PurchasedCreationController()
    return purchasedCreationController.get_purchased_creations(user_id)

@creation_bp.route('/purchesed-details', methods=['GET'])
@safe_route
@require_user
def get_purchesed_creation_details():
    user_id = getattr(request, 'user_id', None)
    creation_id = request.args.get('creation_id')
    purchasedCreationController = PurchasedCreationController()
    return purchasedCreationController.get_purchased_creation_details(user_id,creation_id)



#recently added creation routes
@creation_bp.route('/recentCreations/page/<page>/perPage/<perPage>', methods=['GET'])
@safe_route
def recentCreations(page,perPage):
    current_user_id = getattr(request, 'user_id', None)
    obj = RecentlyAddedCreationController()
    return obj.getRecentlyAddedCreations(int(page),int(perPage),current_user_id)

# trending creation routes
@creation_bp.route('/trendingCreations/page/<page>/perPage/<perPage>', methods=['GET'])
@safe_route
def trendingCreations(page,perPage):
    current_user_id = getattr(request, 'user_id', None)
    obj = TrendingCreationController()
    return obj.getTrendingCreations(int(page),int(perPage),current_user_id)
