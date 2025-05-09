
from flask import Blueprint, request
from app.creation_manegement.controller.purchesed_creation_controller import PurchasedCreationController


creation_bp = Blueprint('creation', __name__, url_prefix='/creation')

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

