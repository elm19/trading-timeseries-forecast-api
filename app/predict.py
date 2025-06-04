from flask import Blueprint, jsonify, request
from datetime import datetime
from . import db
from sqlalchemy import text

predict = Blueprint('predict', __name__)

@predict.route('/predict')
def home():
    # Get the date from query parameters or use the current date
    date = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))

    # Get the model_id from query parameters or use the default value of 1
    model_id = request.args.get('model_id', 1)

    # Query the models_signal table for the specified date and model_id
    try:
        with db.engine.connect() as connection:
            query = text("SELECT * FROM models_prediction WHERE date = :date AND model_id = :model_id")
            result = connection.execute(query, {"date": date, "model_id": model_id}).fetchall()

        if result:
            # Convert the result to a list of dictionaries
            predictions = [dict(row._mapping) for row in result]
            return jsonify(predictions)
        else:
            return jsonify({"error": "No predictions found for the specified date and model."}), 404
    except Exception as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
