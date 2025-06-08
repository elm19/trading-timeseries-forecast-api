from flask import Blueprint, jsonify, abort
from sqlalchemy import text
import os
from datetime import datetime
from . import db

model_info = Blueprint('model_info', __name__)


@model_info.route('/model-info')
def home():
    try:
        with db.engine.connect() as connection:
            query = text("SELECT * FROM model_info")
            result = connection.execute(query).fetchall()

        if result:
            models = [dict(row._mapping) for row in result]
            return jsonify({
                "models": models,
                "total_models": len(models),
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            })
        else:
            return jsonify({"error": "No models found in the database."}), 404
    except Exception as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500

@model_info.route('/model-info/<model_id>')
def get_model_info(model_id):
    try:
        with db.engine.connect() as connection:
            query = text("SELECT * FROM model_info WHERE modelid = :model_id")
            result = connection.execute(query, {"model_id": model_id}).fetchone()

        if result:
            model_data = dict(result._mapping)
            return jsonify({
                "model": model_data,
                "status": "available",
                "last_checked": datetime.now().isoformat()
            })
        else:
            return jsonify({"error": f"Model with ID '{model_id}' not found."}), 404
    except Exception as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500

@model_info.route('/market', defaults={'market_name': None})
@model_info.route('/market/<market_name>')
def get_models_or_markets(market_name):
    try:
        with db.engine.connect() as connection:
            if market_name:
                # Query models for the specified market
                query = text("SELECT * FROM model_info WHERE market = :market_name")
                result = connection.execute(query, {"market_name": market_name}).fetchall()

                if result:
                    models = [dict(row._mapping) for row in result]
                    return jsonify({
                        "market": market_name,
                        "models": models,
                        "total_models": len(models),
                        "last_checked": datetime.now().isoformat()
                    })
                else:
                    return jsonify({"error": f"No models found for market '{market_name}'."}), 404
            else:
                # Query all available markets
                query = text("SELECT DISTINCT market FROM model_info")
                result = connection.execute(query).fetchall()

                if result:
                    markets = [row[0] for row in result]
                    return jsonify({
                        "available_markets": markets,
                        "total_markets": len(markets),
                        "last_checked": datetime.now().isoformat()
                    })
                else:
                    return jsonify({"error": "No markets found in the database."}), 404
    except Exception as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500


