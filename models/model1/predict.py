import joblib
import json
import numpy as np
from keras.models import load_model
from collections import Counter
import pandas as pd
import yfinance as yf
from keras.utils import to_categorical
import pandas_ta as ta
import requests
import matplotlib.pyplot as plt

api_link = "https://elm19.pythonanywhere.com/"
# Define the process function
def treat(df):
    # Adjust column names to match Yahoo Finance data structure
    df.rename(columns={"Adj Close": "close", "Open": "open", "High": "high", "Low": "low", "Volume": "volume"}, inplace=True)
    return df

def indicators(df):
    # Add several technical indicators
    df['SMA_20'] = ta.sma(df['close'], length=20)  # 50-day Simple Moving Average
    df['RSI'] = ta.rsi(df['close'], length=14)  # Relative Strength Index (14-day)
    df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)  # Average True Range
    df.ta.macd(append=True)

    df.dropna(inplace=True)
    return df

def add_target(df, lookahead=5):
    df = df.copy()
    closes = df['close'].values
    atrs   = df['ATR'].values
    n      = len(df)
    targets = np.zeros(n, dtype=int)

    for i in range(n):
        up_thresh   = closes[i] + 1.5 * atrs[i]
        down_thresh = closes[i] - 1.5 * atrs[i]
        for future_close in closes[i+1 : i+1+lookahead]:
            if future_close >= up_thresh:
                targets[i] = 1
                break
            elif future_close <= down_thresh:
                targets[i] = -1
                break

    df['target'] = targets
    return df

def standardize(df, scaler=None):
    df = df.copy()
    features = df.drop(columns=['target']) if 'target' in df.columns else df
    
    scaled = scaler.transform(features)
    scaled_df = pd.DataFrame(scaled, columns=features.columns, index=df.index)
    if 'target' in df.columns:
        scaled_df['target'] = df['target'].values

    return scaled_df

def sequence(df, seq_len=20):
    target = df['target']
    target_map = {-1: 0, 0: 1, 1: 2}
    y = target.map(target_map).values

    X, Y = [], []
    for i in range(seq_len, len(df)):
        X.append(df[i-seq_len:i])
        Y.append(y[i])

    X = np.array(X)
    Y = to_categorical(Y, num_classes=3)

    return X, Y

def process(df_raw, scaler, dev = True, ind=True):
    df = df_raw.copy()
    if dev: 
        df = treat(df)
    if ind:
        df = indicators(df)
    df = add_target(df, lookahead=7)
    df = standardize(df, scaler=scaler)
    X, Y = sequence(df)
    return X, Y

# Fetch latest 54 data points for gold futures market from Yahoo Finance
data = yf.download('GC=F', period='54d', interval='1d', auto_adjust=False)
data.reset_index(inplace=True)
print("Data fetched:", data.head())
# Load scaler
scaler = joblib.load('models/model1/scaler.pkl')

# Process data
X, Y = process(data, scaler, dev=True)

# Load model
model = load_model('models/model1/regulized_model.h5')

# Predict
proba = model.predict(X)
pred_ix = np.argmax(proba, axis=1)

# Map predictions to labels
class_map = {0: 'sell', 1: 'hold', 2: 'buy'}
pred_labels = [class_map[i] for i in pred_ix]

# Count buy signals
counts = Counter(pred_labels)
print("Counts:", counts)

# Send predictions to API
api_url = api_link + "/save-predictions"
headers = {"Content-Type": "application/json"}

for date, proba, label in zip(data['Date'][-len(pred_labels):], proba, pred_labels):
    payload = {
        "date": date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "modelid": "model1",
        "prediction": label,
        "proba_buy": float(proba[2]),
        "proba_hold": float(proba[1]),
        "proba_sell": float(proba[0])
    }
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Successfully sent prediction for {date}")
    else:
        print(f"Failed to send prediction for {date}: {response.text}")

# Plot the predictions
plt.figure(figsize=(10, 6))
plt.plot(data['Date'][-len(pred_labels):], [proba[i][2] for i in range(len(proba))], label='Buy Probability', color='green')
plt.plot(data['Date'][-len(pred_labels):], [proba[i][1] for i in range(len(proba))], label='Hold Probability', color='blue')
plt.plot(data['Date'][-len(pred_labels):], [proba[i][0] for i in range(len(proba))], label='Sell Probability', color='red')
plt.xlabel('Date')
plt.ylabel('Probability')
plt.title('Prediction Probabilities')
plt.legend()
plt.grid()
plt.show()

# Plot the head of the imported data
plt.figure(figsize=(10, 6))
data.head().plot(kind='bar', x='Date', y=['open', 'high', 'low', 'close'], title='Market Data Head')
plt.show()
