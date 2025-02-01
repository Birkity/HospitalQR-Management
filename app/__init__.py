from flask import Flask
from .config import Config
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Import and register blueprints correctly
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    CSRFProtect(app)

    # Initialize ChapaPayment globally
    from .services.payment_gateway import ChapaPayment
    app.config['CHAPA_API'] = ChapaPayment()

    return app
