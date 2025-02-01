from flask import Flask
from .config import Config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from .models import User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.template_folder = 'static/templates'

    # Import and register blueprints correctly
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    CSRFProtect(app)

    # Initialize ChapaPayment globally
    from .services.payment_gateway import ChapaPayment
    app.config['CHAPA_API'] = ChapaPayment()

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        user_data = User.find_by_id(user_id)
        if user_data:
            return User.create_from_db(user_data)
        return None

    return app
