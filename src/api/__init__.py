from flask import Flask
from .routes.metrics import metrics_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(metrics_blueprint, url_prefix='/metrics')
    return app
