from flask import Blueprint, jsonify, request
from sqlalchemy import text
from . import db

trades = Blueprint('trades', __name__)

@trades.route('/trades')
def get_trades():
    # Get the model_id from query parameters
    model_id = request.args.get('modelid')
    if not model_id:
        return jsonify({"error": "modelid parameter is required."}), 400

    # Get the range parameter (default is 0 for the last 100 trades)
    range_param = int(request.args.get('range', 0))

    # Calculate the offset and limit based on the range parameter
    offset = range_param * 100
    limit = 100

    try:
        with db.engine.connect() as connection:
            # Query to get the total number of trades for the model
            total_query = text("SELECT COUNT(*) AS total_trades FROM trades WHERE modelid = :modelid")
            total_result = connection.execute(total_query, {"modelid": model_id}).fetchone()
            total_trades = total_result[0] if total_result else 0

            # Query to get the trades within the specified range
            trades_query = text("SELECT * FROM trades WHERE modelid = :modelid ORDER BY entry_date DESC LIMIT :limit OFFSET :offset")
            trades_result = connection.execute(trades_query, {"modelid": model_id, "limit": limit, "offset": offset}).fetchall()

            if trades_result:
                trades = [dict(row._mapping) for row in trades_result]
                return jsonify({
                    "modelid": model_id,
                    "trades": trades,
                    "total_trades": total_trades
                })
            else:
                return jsonify({"error": "No trades found for the specified model and range."}), 404
    except Exception as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
