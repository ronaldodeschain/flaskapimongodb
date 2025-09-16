from flask import Flask
from .routes.main import main_bp
from .routes.categoria_bp import categoria_bp 



def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(categoria_bp)
    return app