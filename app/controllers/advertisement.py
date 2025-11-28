from flask import Blueprint, request
from model.advertisement import AdvertisementModel
from app.utils.decorators import safe_route, require_user

advertisement_ctrl = Blueprint('advertisement_ctrl', __name__)


@advertisement_ctrl.route('/advertisements', methods=['GET'])
@safe_route
def getAdvertisements():
    current_user_id = getattr(request, 'user_id', None)
    return AdvertisementModel().get_advertisements_by_location(current_user_id, request.args.get('location'))


@advertisement_ctrl.route('/advertisements/add', methods=['POST'])
@safe_route
@require_user
def addNewAdvertisment():
    return AdvertisementModel().add_advertisement(request)
