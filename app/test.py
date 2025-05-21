from flask import Blueprint, jsonify
from datetime import datetime

test = Blueprint('test', __name__)

@test.route('/test')
def see():
    dummy_response = {
        "test_status": "success",
        "timestamp": datetime.now().isoformat(),
        "environment": {
            "name": "development",
            "python_version": "3.8",
            "flask_version": "3.1.0"
        },
        "test_results": {
            "api_health": "ok",
            "database_connection": "ok",
            "model_loading": "ok"
        }
    }
    return jsonify(dummy_response)
