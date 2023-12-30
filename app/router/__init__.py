from flask import Flask
from .embedding import embedding_blueprint

def register_blueprints(app: Flask):
    app.register_blueprint(embedding_blueprint, url_prefix='/embedding')