from flask import Flask
from .document import document_blueprint

def register_blueprints(app: Flask):
    app.register_blueprint(document_blueprint, url_prefix='/docs')