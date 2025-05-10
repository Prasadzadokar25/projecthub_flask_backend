from flask import Flask, jsonify
from model.advertisement import AdvertisementModel
from model.category_model import categoryModel
from model.order_medel import OrderModel
from model.reels_model import ReelsModel
from model.search_model import SearchModel
from model.transactions_model import TransactionModel
from model.login_model import LoginModel
from model.creation_model import CreationModel
from flask import request,send_file
from datetime import datetime
import uuid
import os
from flask_cors import CORS
from app.register_blueprint import register_blueprint


app = Flask(__name__)

CORS(app)
register_blueprint(app)


@app.route("/")
def welcome():
    return "hello welcome to projecthub"


@app.route("/checkLogin",methods=["POST"])
def checkLogin():
    userobj = LoginModel()
    data = request.get_json()
    return userobj.checkLoginDetailsModel(data)

# creation_controller.py



@app.route('/creation/purched/page/<page>/perPage/<perPage>/uid/<uid>', methods=['GET'])
def purchedCreations(page,perPage,uid):
    obj = CreationModel()
    return obj.getPurchedCreations(int(page),int(perPage),uid)

@app.route('/creations/page/<page>/perPage/<perPage>/uid/<uid>', methods=['GET'])
def getCreations(page,perPage,uid):
    obj = CreationModel()
    return obj.getCreationsModel(int(page),int(perPage),uid)

@app.route('/recentCreations/page/<page>/perPage/<perPage>/uid/<uid>', methods=['GET'])
def recentCreations(page,perPage,uid):
    obj = CreationModel()
    return obj.getRecentlyAddedCreations(int(page),int(perPage),uid)


@app.route('/trendingCreations/page/<page>/perPage/<perPage>/uid/<uid>', methods=['GET'])
def trendingCreations(page,perPage,uid):
    obj = CreationModel()
    return obj.getTrendingCreations(int(page),int(perPage),uid)

@app.route('/recomandedCreations/page/<page>/perPage/<perPage>/uid/<uid>', methods=['Post'])
def getRecomandedCreations(page,perPage,uid):
    obj = CreationModel()
    return obj.getTrendingCreations(int(page),int(perPage),uid)

@app.route('/creation/card/add', methods=['POST'])
def addCreationInUserCard():
    data = request.get_json()
    obj = CreationModel()
    return obj.addCreationInUserCard(data)

@app.route('/creation/card/remove', methods=['POST'])
def removeFromCart():
    data = request.get_json()
    obj = CreationModel()
    return obj.removeFromCart(data)

@app.route('/creation/card/get/userid/<uid>', methods=['GET'])
def getInCardCreations(uid):
    obj = CreationModel()
    return obj.getInCardCreation(uid)


# order_controller.py
@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.get_json()
    obj = OrderModel()
    return obj.create_order(data)


# file_controller.py
@app.route("/app/uploads/creation/thumbnail/<filename>",methods=['GET'])
def getthumbnail(filename):
    return send_file(f"app/uploads/creation/thumbnail/{filename}")

@app.route("/uploads/profilePick/<filename>",methods=['GET'])
def getProfilePhoto(filename):
    return send_file(f"app/uploads/profilePick/{filename}")

@app.route("/uploads/categories/<filename>",methods=['GET'])
def getCategories(filename):
    return send_file(f"app/uploads/categories/{filename}")

@app.route("/uploads/advertisements/ad_images/<filename>",methods=['GET'])
def getAdImage(filename):
    return send_file(f"app/uploads/advertisements/ad_images/{filename}")


@app.route('/app/uploads/creation/sourcefile/<filename>', methods=['GET'])
def download_file(filename):
    # Path to your ZIP file
    file_path = f'uploads/creation/sourcefile/{filename}'

    try:
        # Send the file to the client
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e), 404

# categories_controller.py
@app.route('/categories/<uid>', methods=['GET'])
def get_categories(uid):
    category_Model = categoryModel()
    try:
        categories = category_Model.getCategories(1)  # Replace 1 with dynamic user ID if needed

        if categories:
            return jsonify({"status": "success", "data": categories}), 200  # HTTP 200 OK
        else:
            return jsonify({"status": "error", "message": "No categories found"}), 404  # HTTP 404 Not Found

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500  # HTTP 500 Internal Server Error

# Import the controllers to register routes


@app.route('/reels', methods=['GET'])
def getReels():
    return ReelsModel().get_reels(request)

@app.route('/reel/addLike', methods=['POST'])
def addLike():
    return ReelsModel().addLike( request.get_json())

@app.route('/reel/removeLike', methods=['POST'])
def removeLike():
    return ReelsModel().removeLike( request.get_json())

@app.route('/transactions', methods=['GET'])
def getTransactions():
    return TransactionModel().fetchTransaction(int(request.args.get('user_id', 1)))

@app.route('/reel/likes', methods=['GET'])
def getLikeInfo():
    return ReelsModel().get_like_info(request)

@app.route('/search/creation', methods=['GET'])
def getSearchedCreations():
    return SearchModel().get_serched_Creations(request)

# advertisement_controller.py
@app.route('/advertisements', methods=['GET'])
def getAdvertisements():
    return AdvertisementModel().get_advertisements_by_location(request.args.get('user_id', 1),request.args.get('location'))


@app.route('/advertisements/add', methods=['POST'])
def addNewAdvertisment():
    return AdvertisementModel().add_advertisement(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
