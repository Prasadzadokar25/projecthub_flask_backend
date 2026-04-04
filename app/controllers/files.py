from flask import Blueprint, send_file, request


files_ctrl = Blueprint('files_ctrl', __name__)


@files_ctrl.route('/uploads/creation/thumbnail/<filename>', methods=['GET'])
def getthumbnail(filename):
    return send_file(f"uploads/creation/thumbnail/{filename}")


@files_ctrl.route('/uploads/profilePick/<filename>', methods=['GET'])
def getProfilePhoto(filename):
    return send_file(f"uploads/profilePick/{filename}")


@files_ctrl.route('/uploads/categories/<filename>', methods=['GET'])
def getCategories(filename):
    return send_file(f"uploads/categories/{filename}")


@files_ctrl.route('/uploads/advertisements/ad_images/<filename>', methods=['GET'])
def getAdImage(filename):
    return send_file(f"app/uploads/advertisements/ad_images/{filename}")


@files_ctrl.route('/app/uploads/creation/sourcefile/<filename>', methods=['GET'])
def download_file(filename):
    file_path = f'app/uploads/creation/sourcefile/{filename}'
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e), 404
