from flask import Blueprint

# Define blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
main_bp = Blueprint('main', __name__)

# Import route files (this ensures routes get registered)
from . import auth, main
