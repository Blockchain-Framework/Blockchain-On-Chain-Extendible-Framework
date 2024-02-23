from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Flask-Limiter without attaching to an app
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


def init_app_with_limiter(app):
    # Attach the limiter to the app
    limiter.init_app(app)
