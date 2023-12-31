from flask import Flask
from .document import document_blueprint
from .chat import chat_blueprint

def register_blueprints(app: Flask):
    app.register_blueprint(document_blueprint, url_prefix='/docs')
    app.register_blueprint(chat_blueprint, url_prefix='/chat')