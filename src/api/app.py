from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.metric import metrics_blueprint

import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_CONNECTION")
    db = SQLAlchemy(app)
    app.register_blueprint(metrics_blueprint, url_prefix='/metrics')
    return app