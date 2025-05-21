from flask import Blueprint, jsonify, abort
import os
from datetime import datetime

model_info = Blueprint('model_info', __name__)

# Dictionary to store model information (in a real app, this would come from a database)
MODELS = {
    'lstm': {
        "id": "lstm",
        "type": "LSTM",
        "last_trained": "2025-05-20",
        "accuracy": 0.89,
        "parameters": {
            "layers": 3,
            "units": 64,
            "dropout": 0.2
        },
        "backtest_metrics": {
            "sharpe_ratio": 2.45,
            "max_drawdown_pct": -15.3,
            "win_rate_pct": 68.5,
            "total_return_pct": 145.8,
            "annual_return_pct": 32.4,
            "volatility_pct": 18.2,
            "sortino_ratio": 2.85,
            "trades_per_month": 42,
            "avg_holding_period_days": 3.5,
            "backtest_period": {
                "start": "2024-01-01",
                "end": "2025-05-20"
            }
        }
    },
    'gru': {
        "id": "gru",
        "type": "GRU",
        "last_trained": "2025-05-19",
        "accuracy": 0.87,
        "parameters": {
            "layers": 2,
            "units": 32,
            "dropout": 0.1
        },
        "backtest_metrics": {
            "sharpe_ratio": 2.12,
            "max_drawdown_pct": -18.7,
            "win_rate_pct": 65.2,
            "total_return_pct": 128.3,
            "annual_return_pct": 29.8,
            "volatility_pct": 19.5,
            "sortino_ratio": 2.45,
            "trades_per_month": 38,
            "avg_holding_period_days": 4.2,
            "backtest_period": {
                "start": "2024-01-01",
                "end": "2025-05-19"
            }
        }
    }
}

@model_info.route('/model-info')
def home():
    dummy_response = {
        "models": list(MODELS.values()),
        "total_models": len(MODELS),
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    return jsonify(dummy_response)

@model_info.route('/model-info/<model_name>')
def get_model_info(model_name):
    model_name = model_name.lower()
    if model_name not in MODELS:
        abort(404, description=f"Model '{model_name}' not found")
    
    model_path = os.path.join(os.path.dirname(__file__), 'models', model_name)
    
    # In a real application, you would load the model's metadata from the model file
    # or a database. For now, we'll return the dummy data
    model_data = MODELS[model_name]
    
    return jsonify({
        "model": model_data,
        "path": model_path,
        "status": "available",
        "last_checked": datetime.now().isoformat()
    })
