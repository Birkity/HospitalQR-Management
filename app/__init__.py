from flask import Flask
from .config import Config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from .models import User
from .services.payment_gateway import ChapaPayment

csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='static/templates')
    app.config.from_object(Config)

    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        user_data = User.find_by_id(user_id)
        if user_data:
            return User.create_from_db(user_data)
        return None

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    return app
