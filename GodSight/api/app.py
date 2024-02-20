from flask import Flask
from flask_cors import CORS
import sys
import os
from flasgger import Swagger

from .database.database import db
from .routes.metric import metrics_blueprint
from .routes.init import init_blueprint
from dotenv import load_dotenv

load_dotenv()

# Rest of your code...

def create_app(config=None):
    app = Flask(__name__)
    CORS(app)
    # Configure app
    Swagger(app)

    if config:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}"
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_CONNECTION")
    
    # Initialize the SQLAlchemy instance with the app
    db.init_app(app)

    app.register_blueprint(metrics_blueprint, url_prefix='/metrics')
    app.register_blueprint(init_blueprint, url_prefix='/init')

    @app.route('/')
    def welcome():
        return 'Welcome GodSight'

    return app