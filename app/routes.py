from flask import Blueprint, Response
from . import db
from sqlalchemy import text
import json 

main = Blueprint('main', __name__)

@main.route('/')
def home():
    response_data = {
        "api_status": "healthy",
        "endpoints": {
            "/": "API status and available endpoints",
            "/predict": "Get predictions for a specific model and date (or the latest date if not specified)",
            "/predict/model?all=true": "Get all predictions for a specific model",
            "/model-info": "Get information about all models",
            "/model-info/model_id": "Get information about a specific model by its ID",
            "/market": "Get all available markets",
            "/market/market_name": "Get models for a specific market",
            "/trades": "Get trades for a specific model, with pagination support"
        }
    }
    return Response(json.dumps(response_data, ensure_ascii=False), mimetype='application/json')


@main.route('/test-db')
def test_db_connection():
    try:
        # Attempt to connect to the database
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return "Database connection successful!", 200
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500
