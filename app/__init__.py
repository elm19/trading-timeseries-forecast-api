from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Database configuration
    import os
    from dotenv import load_dotenv

    # Load environment variables from a .env file
    load_dotenv()

    # Database configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    from .routes import main
    from .predict import predict
    from .model_info import model_info
    from .trades import trades

    app.register_blueprint(main)
    app.register_blueprint(predict)
    app.register_blueprint(model_info)
    app.register_blueprint(trades)

    return app
