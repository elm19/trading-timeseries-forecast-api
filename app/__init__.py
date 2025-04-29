from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import main
    from .predict import predict
    from .model_info import model_info

    app.register_blueprint(main)
    app.register_blueprint(predict)
    app.register_blueprint(model_info)
    return app
