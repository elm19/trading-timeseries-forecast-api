# Trading Time Series Forecast API

A Flask-based REST API for time series forecasting in trading applications. This API provides access to different machine learning models (LSTM, GRU) for trading predictions and analysis.

## Features

- Multiple model support (LSTM, GRU)
- Real-time predictions
- Detailed model information and metrics
- Comprehensive backtest results
- Model performance monitoring

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd trading-timeseries-forecast-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the development server:
```bash
python run.py
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints

### 1. Home Endpoint
- **URL:** `/`
- **Method:** `GET`
- **Description:** Returns API information and available endpoints
- **Response Example:**
```json
{
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
```

### 2. Prediction Endpoint
- **URL:** `/predict`
- **Method:** `GET`
- **Description:** Returns trading predictions for the current date
- **Response Example:**
```json
{
    "prediction_date": "2025-05-21",
    "model_used": "model1",
    "prediction": {
        "signal": "buy",
        "confidence": 0.85
    }
}
```

### 3. Model Information Endpoints

#### List All Models
- **URL:** `/model-info`
- **Method:** `GET`
- **Description:** Returns information about all available models
- **Response Example:**
```json
{
    "models": [
        {
            "id": "lstm",
            "type": "LSTM",
            "accuracy": 0.89,
            "backtest_metrics": {
                "sharpe_ratio": 2.45,
                "win_rate_pct": 68.5
            }
        }
    ],
    "total_models": 2,
    "last_updated": "2025-05-21"
}
```

#### Single Model Information
- **URL:** `/model-info/<model_name>`
- **Method:** `GET`
- **Description:** Returns detailed information about a specific model
- **Parameters:** 
  - `model_name`: Name of the model (e.g., "lstm" or "gru")
- **Response Example:**
```json
{
    "model": {
        "id": "lstm",
        "type": "LSTM",
        "parameters": {
            "layers": 3,
            "units": 64,
            "dropout": 0.2
        },
        "backtest_metrics": {
            "sharpe_ratio": 2.45,
            "max_drawdown_pct": -15.3,
            "win_rate_pct": 68.5,
            "total_return_pct": 145.8
        }
    },
    "status": "available",
    "last_checked": "2025-05-21T10:00:00.000Z"
}
```

## Model Performance Metrics

The API provides comprehensive backtest metrics for each model:

1. **Performance Indicators**
   - Sharpe Ratio: Risk-adjusted return metric
   - Sortino Ratio: Downside risk-adjusted return metric
   - Max Drawdown: Largest peak-to-trough decline
   - Win Rate: Percentage of profitable trades
   - Total Return: Overall return percentage
   - Annual Return: Annualized return percentage
   - Volatility: Price volatility percentage

2. **Trading Statistics**
   - Trades per Month: Average number of trades executed monthly
   - Average Holding Period: Mean duration of holding positions

## Error Handling

The API uses standard HTTP status codes:
- 200: Successful request
- 404: Model or resource not found
- 500: Server error

## Development

The project structure is organized as follows:
```
trading-timeseries-forecast-api/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── predict.py
│   ├── model_info.py
│   ├── models/
│   └── utils/
├── requirements.txt
└── run.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]
