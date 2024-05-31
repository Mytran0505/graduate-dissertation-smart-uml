from flask import Flask
from .route import UML_DDL
def create_app():
    app = Flask(__name__)
    app.register_blueprint(UML_DDL)
    return app