from flask import Flask
from flask_cors import CORS
from .config import Config
from app.register_blueprint import register_blueprint
from app.auth import register_auth
from model.sqlalchemy_models import Base, engine


def create_app(config_object=None):
    app = Flask(__name__)

    # load config
    if config_object is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(config_object)

    # Enable CORS
    CORS(app)

    # Create DB tables if models present (keeps previous behavior)
    try:
        Base.metadata.create_all(engine)
    except Exception:
        # if SQLAlchemy not configured, ignore at startup
        pass

    # Register blueprints and auth
    register_blueprint(app)
    register_auth(app)

    return app
