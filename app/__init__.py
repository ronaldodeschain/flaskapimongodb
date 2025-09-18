from flask import Flask
from .database import mongo
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Check for required configurations
    if not app.config.get("MONGO_URI"):
        raise RuntimeError("MONGO_URI environment variable is not set.")
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY environment variable is not set.")

    mongo.init_app(app)
    
    # Import and register blueprints here to avoid circular imports
    from .routes.main import main_bp
    from .routes.categoria_bp import categoria_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(categoria_bp)
    return app