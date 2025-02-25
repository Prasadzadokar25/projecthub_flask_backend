# from flask import jsonify
# from app import app
# from model.category_model import categoryModel

# @app.route('/categories', methods=['GET'])
# def get_categories():
#     category_Model = categoryModel()
#     try:
#         categories = category_Model.getCategories(1)  # Replace 1 with dynamic user ID if needed
        
#         if categories:
#             return jsonify({"status": "success", "data": categories}), 200  # HTTP 200 OK
#         else:
#             return jsonify({"status": "error", "message": "No categories found"}), 404  # HTTP 404 Not Found
    
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500  # HTTP 500 Internal Server Error
