from flask import Blueprint, jsonify
from . import db
from sqlalchemy import text

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

@main.route('/test-db')
def test_db_connection():
    try:
        # Attempt to connect to the database
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return "Database connection successful!", 200
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500
