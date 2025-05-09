from flask import Blueprint, request
from app.bank_account_manegment.controller.bank_account_controller import BackAcountController

bank_account_bp = Blueprint('bank_account', __name__, url_prefix='/bank-account')


# bank_account_controller.py
@bank_account_bp.route('/add', methods=['POST'])
def add_bank_account():
    data = request.get_json()
    obj =BackAcountController()
    return obj.add_bank_account(data)

@bank_account_bp.route('/get', methods=['GET'])
def get_accounts_for_user():
    user_id = request.args.get('user_id')
    obj =BackAcountController()
    return obj.get_accounts_for_user(user_id)

@bank_account_bp.route('/set-primary/<int:user_id>/<int:account_id>', methods=['PUT'])
def set_primary_account(user_id, account_id):
    obj = BackAcountController()
    return obj.set_primary_account(user_id,account_id)