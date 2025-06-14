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
api_link = 'https://elm19.pythonanywhere.com/'
data_t = yf.download('GC=F', period='80d')[['Open', 'High', 'Low', 'Close', 'Volume']]
data_t = data_t.rename(columns={'Close': 'close', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Volume': 'volume'})
data_t = data_t.reset_index().rename(columns={'Date': 'Date'})


data_t.columns.name = None
data_t.columns = data_t.columns.droplevel(1)  # removes the Ticker level


if data_t.empty or data_t.isnull().all().all():
    print("Download failed or returned no usable data.  using another source")
    data_t = pd.read_csv('models/model1/data.csv', parse_dates=['Date'])

df = data_t[["Date", "close", "open", "high", "low", "volume"]]

df = df.set_index('Date')  # set 'Date' as index
df.index.name = 'Date'  # optional: name the index explicitly
df.columns.name = None
print("data imported", df.head())


def indicators(df):
    # Add several technical indicators
    df['SMA_20'] = ta.sma(df['close'], length=20)  # 50-day Simple Moving Average
    df['RSI'] = ta.rsi(df['close'], length=14)  # Relative Strength Index (14-day)
    df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)  # Average True Range
    df.ta.macd(append=True)

    df.dropna(inplace=True)
    return df
    
df = indicators(df)
print("Indicators added check")


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
df = add_target(df)
print("Target added check")

def standardize(df, scaler=None):
    df = df.copy()
    features = df.drop(columns=['target']) if 'target' in df.columns else df
    scaled = scaler.transform(features)
    scaled_df = pd.DataFrame(scaled, columns=features.columns, index=df.index)
    if 'target' in df.columns:
        scaled_df['target'] = df['target'].values

    return scaled_df

# Load scaler
scaler = joblib.load('models/model1/scaler.pkl')
# Process data
df = standardize(df, scaler)
print("Data standardized check")

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
X, y = sequence(df)
print("Data sequenced check")

# Load model
model = load_model('models/model1/regulized_model.keras')
proba = model.predict(X)
pred_ix = np.argmax(proba, axis=1)
print("Model predictions made check")
# Map predictions to labels
class_map = {0: 'sell', 1: 'hold', 2: 'buy'}
pred_labels = [class_map[i] for i in pred_ix]

print("test",pred_labels[-1], proba[-1])
# Send predictions to API
api_url = api_link + "/save-predictions"
headers = {"Content-Type": "application/json"}
print(df.index[-1].strftime('%Y-%m-%d'))

payload = {
    "date": df.index[-1].strftime('%Y-%m-%d'),
    "modelid": "model1",
    "prediction": pred_labels[-1],
    "proba_buy": float(proba[-1][2]),
    "proba_hold": float(proba[-1][1]),
    "proba_sell": float(proba[-1][0])
}
print(payload)
response = requests.post(api_url, json=payload, headers=headers)
if response.status_code == 200:
    print(f"Successfully sent prediction for {df.index[-1].strftime('%Y-%m-%d'),}")
else:
    print(f"Failed to send prediction for {df.index[-1].strftime('%Y-%m-%d'),}: {response.text}")
