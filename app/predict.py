from flask import Blueprint, jsonify
from datetime import datetime

predict = Blueprint('predict', __name__)

@predict.route('/predict')
def home():
    dummy_response = {
        "prediction_date": datetime.now().strftime("%Y-%m-%d"),
        "model_used": "model1",
        "prediction": {
            "signal": "buy",
            "confidence": 0.85
        }
    }
    return jsonify(dummy_response)
