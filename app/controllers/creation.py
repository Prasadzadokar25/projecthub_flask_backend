from flask import Blueprint, request
from model.creation_model import CreationModel
from app.utils.decorators import safe_route, require_user

creation_ctrl = Blueprint('creation_ctrl', __name__)


@creation_ctrl.route('/creations/page/<page>/perPage/<perPage>', methods=['GET'])
@safe_route
def getCreations(page, perPage):
    # Use the authenticated user id from the JWT (set on request by auth.register_auth)
    current_user_id = getattr(request, 'user_id', None)
    obj = CreationModel()
    return obj.getCreationsModel(int(page), int(perPage), current_user_id)


@creation_ctrl.route('/recomandedCreations/page/<page>/perPage/<perPage>', methods=['POST'])
@safe_route
def getRecomandedCreations(page, perPage):
    current_user_id = getattr(request, 'user_id', None)
    obj = CreationModel()
    return obj.getTrendingCreations(int(page), int(perPage), current_user_id)


@creation_ctrl.route('/creation/card/add', methods=['POST'])
@safe_route
@require_user
def addCreationInUserCard():
    data = request.get_json() or {}
    # ensure the user id in payload (model expects userId) matches token
    data['userId'] = getattr(request, 'user_id', None)
    obj = CreationModel()
    return obj.addCreationInUserCard(data)


@creation_ctrl.route('/creation/card/remove', methods=['POST'])
@safe_route
@require_user
def removeFromCart():
    data = request.get_json() or {}
    data['user_id'] = getattr(request, 'user_id', None)
    obj = CreationModel()
    return obj.removeFromCart(data)


@creation_ctrl.route('/creation/card/get', methods=['GET'])
@safe_route
@require_user
def getInCardCreations():
    current_user_id = getattr(request, 'user_id', None)
    obj = CreationModel()
    return obj.getInCardCreation(current_user_id)
