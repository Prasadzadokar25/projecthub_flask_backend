from flask import Blueprint, jsonify, request
from model.category_model import categoryModel
from app.utils.decorators import safe_route

categories_ctrl = Blueprint('categories_ctrl', __name__)


@categories_ctrl.route('/categories', methods=['GET'])
@safe_route
def get_categories():
    category_Model = categoryModel()

    # Validate pagination params
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        if page <= 0 or limit <= 0:
            return jsonify({
                "status": "fail",
                "message": "Page and limit must be positive numbers"
            }), 400

    except ValueError:
        return jsonify({
            "status": "fail",
            "message": "Invalid page or limit value"
        }), 400
        
    print(f"Fetching categories - Page: {page}, Limit: {limit}")

    categories, total = category_Model.getCategories(page, limit)



    # ✔ Data found
    return jsonify({
        "status": "success",
        "page": page,
        "limit": limit,
        "total": total,
        "data": categories
    }), 200

