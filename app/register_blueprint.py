from app.creation.roughts.roughts import creation_bp

def register_blueprint(app):
    app.register_blueprint(creation_bp)
    pass
    """
    Register all blueprints to the main app.
    """
    # from app.api import api_bp
    # from app.auth import auth_bp
    # from app.main import main_bp

    # app.register_blueprint(api_bp)
    # app.register_blueprint(auth_bp)
    # app.register_blueprint(main_bp)