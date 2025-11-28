from flask import Blueprint, request
from app.bank_account_manegment.controller.bank_account_controller import BackAcountController
from app.utils.decorators import safe_route, require_user

bank_account_bp = Blueprint('bank_account', __name__, url_prefix='/bank-account')


# bank_account_controller.py
@bank_account_bp.route('/add', methods=['POST'])
@safe_route
@require_user
def add_bank_account():
    data = request.get_json() or {}
    data['user_id'] = getattr(request, 'user_id', None)
    obj = BackAcountController()
    return obj.add_bank_account(data)


@bank_account_bp.route('/get', methods=['GET'])
@safe_route
@require_user
def get_accounts_for_user():
    user_id = getattr(request, 'user_id', None)
    obj = BackAcountController()
    return obj.get_accounts_for_user(user_id)


@bank_account_bp.route('/set-primary/<int:account_id>', methods=['PUT'])
@safe_route
@require_user
def set_primary_account(account_id):
    user_id = getattr(request, 'user_id', None)
    obj = BackAcountController()
    return obj.set_primary_account(user_id, account_id)