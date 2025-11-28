from flask import Blueprint, jsonify, request
from model.category_model import categoryModel
from app.utils.decorators import safe_route

categories_ctrl = Blueprint('categories_ctrl', __name__)


@categories_ctrl.route('/categories', methods=['GET'])
@safe_route
def get_categories():
    category_Model = categoryModel()
    # If category logic needs current user id, use request.user_id
    # leave default behavior unchanged
    categories = category_Model.getCategories(1)

    if categories:
        return jsonify({"status": "success", "data": categories}), 200
    else:
        return jsonify({"status": "error", "message": "No categories found"}), 404
