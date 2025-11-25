from datetime import timedelta
from flask import Flask, g

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging
from app.config import Config
from app.logging_config import setup_logging

# Initialize Bcrypt and JWTManager
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    # ---- Setup logging ----
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Flask application...") 
    
    # ---- Create Flask app ----
    app = Flask(__name__)
    app.config.from_object(Config)

    # Secret key for sessions
    app.secret_key = Config.SECRET_KEY

    # JWT config
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    jwt.init_app(app)

    # Initialize bcrypt with app
    bcrypt.init_app(app)

    # Enable CORS (optional, if needed for frontend integration)
    CORS(app)

    logger.info("Flask application created successfully")
    return app
