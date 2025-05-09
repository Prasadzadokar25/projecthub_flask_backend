from app.creation_manegement.roughts.roughts import creation_bp
from app.bank_account_manegment.roughts.roughts import bank_account_bp
from app.user_manegment.roughts.roughts import user_bp
def register_blueprint(app):
    app.register_blueprint(creation_bp)
    app.register_blueprint(bank_account_bp)
    app.register_blueprint(user_bp)
    
    """
    Register all blueprints to the main app.
    """
    # from app.api import api_bp
    # from app.auth import auth_bp
    # from app.main import main_bp

    # app.register_blueprint(api_bp)
    # app.register_blueprint(auth_bp)
    # app.register_blueprint(main_bp)