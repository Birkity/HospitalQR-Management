from flask import Flask
from .config import Config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from .models import User
from .services.payment_gateway import ChapaPayment

login_manager = LoginManager()
chapa_payment = ChapaPayment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.template_folder = 'static/templates'

    # Import and register blueprints correctly
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    CSRFProtect(app)

    # Initialize ChapaPayment globally
    chapa_payment.init_app(app)
    app.config['CHAPA_API'] = chapa_payment

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        if not user_id:
            return None
        try:
            user_data = User.find_by_id(user_id)
            if user_data:
                return User.create_from_db(user_data)
            return None
        except Exception as e:
            print(f"Error loading user: {e}")
            return None

    return app
