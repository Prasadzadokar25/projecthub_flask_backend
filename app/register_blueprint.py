from app.controllers.creation import creation_bp
from app.controllers.bank_account import bank_account_bp
from app.controllers.user import user_bp
from app.controllers.auth import auth_bp
from app.controllers.categories import categories_ctrl
from app.controllers.files import files_ctrl

def register_blueprint(app):
    """
    Register all blueprints to the main app.
    """
    app.register_blueprint(creation_bp)
    app.register_blueprint(bank_account_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(categories_ctrl)
    app.register_blueprint(files_ctrl)