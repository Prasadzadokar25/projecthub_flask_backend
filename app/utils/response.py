from flask import jsonify


def ok(data=None, status=200):
    payload = {"status": "success"}
    if data is not None:
        payload['data'] = data
    return jsonify(payload), status


def error(message="Server error", status=500, code=None):
    payload = {"status": "error", "message": message}
    if code is not None:
        payload['code'] = code
    return jsonify(payload), status


def unauthorized(message="Unauthorized"):
    return error(message, status=401)


def bad_request(message="Bad request"):
    return error(message, status=400)
