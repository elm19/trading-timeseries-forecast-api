from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def home():
    dummy_response = {
        "api_status": "healthy",
        "available_endpoints": [
            {
                "path": "/",
                "description": "API information and status"
            },
            {
                "path": "/predict",
                "description": "Get trading predictions"
            },
            {
                "path": "/model-info",
                "description": "Get information about available models"
            }
        ],
        "version": "1.0.0"
    }
    return jsonify(dummy_response)
