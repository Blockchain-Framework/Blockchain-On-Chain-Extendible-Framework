from flask import Flask
from flask_cors import CORS
import sys
import os

from database import db
from routes.metric import metrics_blueprint
<<<<<<< HEAD

=======
from routes.init import init_blueprint
>>>>>>> feature/dual-workflow
from dotenv import load_dotenv

load_dotenv()

# Rest of your code...

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_CONNECTION")
    
    # Initialize the SQLAlchemy instance with the app
    db.init_app(app)

    app.register_blueprint(metrics_blueprint, url_prefix='/metrics')
<<<<<<< HEAD
=======
    app.register_blueprint(init_blueprint, url_prefix='/init')
>>>>>>> feature/dual-workflow
    return app