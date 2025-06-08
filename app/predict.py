from flask import Blueprint, jsonify, request
from datetime import datetime
from . import db
from sqlalchemy import text

predict = Blueprint('predict', __name__)

@predict.route('/predict')
def home():
    # Get the model_id from query parameters or use the default value of 1
    model_id = request.args.get('model_id', 1)

    # Get the date from query parameters or use the latest recorded date
    date = request.args.get('date')

    try:
        with db.engine.connect() as connection:
            if date:
                # Query for the specified date and model_id
                query = text("SELECT * FROM predictions WHERE date = :date AND modelid = :model_id")
                result = connection.execute(query, {"date": date, "model_id": model_id}).fetchone()
            else:
                # Query for the latest recorded date for the specified model_id
                query = text("SELECT * FROM predictions WHERE modelid = :model_id ORDER BY date DESC LIMIT 1")
                result = connection.execute(query, {"model_id": model_id}).fetchone()

            if result:
                # Convert the result to a dictionary
                prediction = dict(result._mapping)
                return jsonify(prediction)
            else:
                return jsonify({"error": "No predictions found for the specified criteria."}), 404
    except Exception as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
