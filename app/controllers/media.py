from flask import Blueprint, request
from model.reels_model import ReelsModel
from model.transactions_model import TransactionModel
from model.search_model import SearchModel
from app.utils.decorators import safe_route, require_user

media_ctrl = Blueprint('media_ctrl', __name__)


@media_ctrl.route('/reels', methods=['GET'])
@safe_route
def getReels():
    current_user_id = getattr(request, 'user_id', None)
    return ReelsModel().get_reels(request, user_id_override=current_user_id)


@media_ctrl.route('/reel/addLike', methods=['POST'])
@safe_route
@require_user
def addLike():
    data = request.get_json() or {}
    data['user_id'] = getattr(request, 'user_id', None)
    return ReelsModel().addLike(data)


@media_ctrl.route('/reel/removeLike', methods=['POST'])
@safe_route
@require_user
def removeLike():
    data = request.get_json() or {}
    data['user_id'] = getattr(request, 'user_id', None)
    return ReelsModel().removeLike(data)


@media_ctrl.route('/transactions', methods=['GET'])
@safe_route
@require_user
def getTransactions():
    current_user_id = getattr(request, 'user_id', None)
    return TransactionModel().fetchTransaction(int(current_user_id))


@media_ctrl.route('/reel/likes', methods=['GET'])
@safe_route
def getLikeInfo():
    current_user_id = getattr(request, 'user_id', None)
    return ReelsModel().get_like_info(request, user_id_override=current_user_id)


@media_ctrl.route('/search/creation', methods=['GET'])
@safe_route
def getSearchedCreations():
    return SearchModel().get_serched_Creations(request)
