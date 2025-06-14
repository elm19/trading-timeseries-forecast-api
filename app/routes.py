from flask import Blueprint, Response, request, jsonify
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


@main.route('/save-predictions', methods=['POST'])
def save_predictions_to_db():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is empty or invalid"}), 400

        # Debugging: Print the received data
        print("Received data:", data)

        # Insert data into the database
        with db.engine.connect() as connection:
            query = text("INSERT INTO predictions (date, modelid, prediction, proba_buy, proba_hold, proba_sell) VALUES (:date, :modelid, :prediction, :proba_buy, :proba_hold, :proba_sell)")
            connection.execute(query, {
                "date": data.get('date'),
                "prediction": data.get('prediction'),
                "modelid": data.get('modelid'),
                "proba_buy": data.get('proba_buy'),
                "proba_hold": data.get('proba_hold'),
                "proba_sell": data.get('proba_sell')
            })
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
