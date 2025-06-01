import requests

url = "https://karaswathi-email-classifier-api.hf.space/classify"
data = {"input_email_body": "Hello, my name is John Doe, and my email is johndoe@example.com."}

response = requests.post(url, json=data)
print(response.status_code)  # Expected: 200 (Success)
print(response.json())  # Expected response structure