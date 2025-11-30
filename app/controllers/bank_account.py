from flask import Blueprint, request, make_response, jsonify
from model.bank_account import BankAccountModel
from app.utils.decorators import safe_route, require_user

bank_account_bp = Blueprint('bank_account', __name__, url_prefix='/bank-account')


# =======================
# CREATE OPERATIONS
# =======================

@bank_account_bp.route('/add', methods=['POST'])
@safe_route
@require_user
def add_bank_account():
    """Add a new bank account for the current user"""
    user_id = getattr(request, 'user_id', None)
    data = request.get_json() or {}
    
    # Validate required fields
    required_fields = ['bank_name', 'account_number', 'ifsc_code']
    for field in required_fields:
        if not data.get(field):
            return make_response({"error": f"Missing required field: {field}"}, 400)
    
    bank_account_model = BankAccountModel()
    result = bank_account_model.create_bank_account(
        user_id,
        data.get('account_holder_name'),
        data.get('bank_name'),
        data.get('account_number'),
        data.get('ifsc_code')
    )
    bank_account_model.close()
    
    if result['success']:
        res = make_response({"message": result['message']}, 201)
    else:
        res = make_response({"error": result['error']}, 400)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


# =======================
# READ OPERATIONS
# =======================

@bank_account_bp.route('/get', methods=['GET'])
@safe_route
@require_user
def get_accounts_for_user():
    """Get all bank accounts for the current user"""
    user_id = getattr(request, 'user_id', None)
    
    bank_account_model = BankAccountModel()
    result = bank_account_model.get_accounts_for_user(user_id)
    bank_account_model.close()
    
    if result['success']:
        res = make_response({"status": "success", "data": result['data']}, 200)
    else:
        res = make_response({"status": "error", "message": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res


# =======================
# UPDATE OPERATIONS
# =======================

@bank_account_bp.route('/set-primary/<int:account_id>', methods=['PUT'])
@safe_route
@require_user
def set_primary_account(account_id):
    """Set a specific account as primary for the current user"""
    user_id = getattr(request, 'user_id', None)
    
    bank_account_model = BankAccountModel()
    result = bank_account_model.set_primary_account(user_id, account_id)
    bank_account_model.close()
    
    if result['success']:
        res = make_response({"message": result['message']}, 200)
    else:
        res = make_response({"error": result['error']}, 500)
    
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res
