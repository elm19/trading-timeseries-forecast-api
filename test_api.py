import requests

# Define the API URL
api_url = "http://127.0.0.1:5000/save-predictions"
headers = {"Content-Type": "application/json"}

# Dummy data for testing
dummy_data = {
    "date": "2026-03-24",
    "prediction": "hold",
    "modelid": "model1",
    "proba_sell": 0.1215985641,
    "proba_hold": 0.7705458999,
    "proba_buy": 0.1078555435
}

# Send the dummy data to the API
response = requests.post(api_url, json=dummy_data, headers=headers)

# Print the response
if response.status_code == 200:
    print("Successfully sent dummy data to the API.")
else:
    print(f"Failed to send dummy data to the API: {response.text}")
