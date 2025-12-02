from flask import Blueprint, request, make_response
from model.login_model import LoginModel
from app.auth import generate_jwt

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/checkLogin', methods=['POST'])
def check_login():
    """Authenticate user and return a JWT token on success.

    This wraps the existing LoginModel.checkLoginDetailsModel call and appends
    a `token` field to the successful response body.
    """
    userobj = LoginModel()
    data = request.get_json()
    # If client sends country_code + phone_number, combine them into user_key
    try:
        if data and isinstance(data, dict):
            cc = data.get('country_code')
            pn = data.get('phone_number')
            if cc and pn and not data.get('user_key'):
                data['user_key'] = f"+{str(cc).lstrip('+')}{pn}"
    except Exception:
        pass

    # call existing login logic which returns a Flask response
    res = userobj.checkLoginDetailsModel(data)
    try:
        if getattr(res, 'status_code', None) == 200:
            body = res.get_json()
            # Expecting body['data'] to be a dict with the user record
            user_id = None
            if body and isinstance(body, dict) and 'data' in body and isinstance(body['data'], dict):
                user_id = body['data'].get('user_id')
            if user_id is not None:
                token = generate_jwt(user_id)
                body['token'] = token
            return make_response(body, 200)
    except Exception as e:
        # fall back to original response when something unexpected happens
        print(f"Token generation error: {str(e)}")
        pass
    return res
