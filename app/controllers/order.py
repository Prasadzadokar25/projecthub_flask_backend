from flask import Blueprint, request
from model.order_medel import OrderModel

order_ctrl = Blueprint('order_ctrl', __name__)


@order_ctrl.route('/create-order', methods=['POST'])
def create_order():
    data = request.get_json()
    obj = OrderModel()
    return obj.create_order(data)
