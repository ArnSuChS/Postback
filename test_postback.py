import requests

url = "http://127.0.0.1:5000/kite_postback"
payload = {
    "order_id": "ABC123",
    "status": "COMPLETE"
}

r = requests.post(url, json=payload)
print("Response:", r.text)

r = requests.get("http://127.0.0.1:5000/view_postbacks")
print("Database contents:", r.json())
