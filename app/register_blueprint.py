from app.creation_manegement.roughts.roughts import creation_bp
from app.bank_account_manegment.roughts.roughts import bank_account_bp
from app.user_manegment.roughts.roughts import user_bp
from app.controllers.auth import auth_bp

def register_blueprint(app):
    """
    Register all blueprints to the main app.
    """
    app.register_blueprint(creation_bp)
    app.register_blueprint(bank_account_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)