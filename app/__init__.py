from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

def create_app():
    app = Flask(__name__)

    # Register Swagger UI blueprint
    SWAGGER_URL = '/docs'  # URL for exposing Swagger UI
    API_URL = '/static/openapi.yaml'  # Our API url (can of course be a local resource)

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Trading Time Series Forecast API",
            'deepLinking': True,
            'displayOperationId': False,
            'displayRequestDuration': True,
            'docExpansion': 'list',
            'showExtensions': False,
            'showCommonExtensions': False,
            'supportedSubmitMethods': ['get'],
            'dom_id': '#swagger-ui',
            'layout': 'BaseLayout',
            # Custom CSS to hide Swagger branding
            'customCss': '''
                .swagger-ui .topbar { display: none }
                .swagger-ui .info .title small { display: none }
                .swagger-ui .info hgroup.main { margin: 0 }
                .swagger-ui .info .title { font-size: 30px }
            '''
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    from .routes import main
    from .predict import predict
    from .model_info import model_info

    app.register_blueprint(main)
    app.register_blueprint(predict)
    app.register_blueprint(model_info)
    return app
