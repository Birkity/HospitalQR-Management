from flask import Flask
from config import Config
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from .routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    CSRFProtect(app)
    
    # Initialize ChapaPayment for global usage within the app context
    from .services.payment_gateway import ChapaPayment
    app.config['CHAPA_API'] = ChapaPayment()

    return app