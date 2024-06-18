from flask import Flask
from .route import UML_DDL, SQL
def create_app():
    app = Flask(__name__)
    app.register_blueprint(UML_DDL)
    app.register_blueprint(SQL)
    return app