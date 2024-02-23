from flask import Flask
from flask_cors import CORS
import os
from flasgger import Swagger

from .database.database import db
from .routes.metric import metrics_blueprint
from .routes.init import init_blueprint
from dotenv import load_dotenv
from .utils.auth import set_api_key
from .limiter import init_app_with_limiter

load_dotenv()


def create_app(config=None):
    app = Flask(__name__)

    """
    use this to avoid DOS attacks

    """

    # init_app_with_limiter(app)

    CORS(app)

    # Configure app
    Swagger(app)

    try:
        secret_key = os.getenv("SECRET_API_KEY") if config is None else config.secret_api_key
        set_api_key(secret_key)
    except ValueError as e:
        # Handle the error (e.g., log it, ignore it, or re-raise it)
        print(e)

    if config:
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}"
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_CONNECTION")

    # Initialize the SQLAlchemy instance with the app
    db.init_app(app)

    app.register_blueprint(metrics_blueprint, url_prefix='/metrics')
    app.register_blueprint(init_blueprint, url_prefix='/init')

    @app.route('/')
    def welcome():
        return 'Welcome GodSight'

    @app.before_request
    def before_request_func():
        # Add general API validations here.
        # For example, you could implement JWT token authentication,
        # IP address filtering, request rate limiting, or other security measures.
        # This is a placeholder for middleware-like functionality that applies to all requests,
        # except for those explicitly excluded.
        pass

    return app