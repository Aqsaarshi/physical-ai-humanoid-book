import requests
import json

# Test the root endpoint
try:
    response = requests.get('http://127.0.0.1:8000/')
    print("Root endpoint response:", response.status_code, response.json())
except Exception as e:
    print("Error accessing root endpoint:", e)

# Test the chat endpoint
try:
    chat_data = {
        "query": "Hello, how are you?",
        "context_mode": "full-book"
    }
    response = requests.post('http://127.0.0.1:8000/api/chat/query',
                           json=chat_data,
                           headers={'Content-Type': 'application/json'})
    print("Chat endpoint response:", response.status_code)
    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print("Response text:", response.text)
except Exception as e:
    print("Error accessing chat endpoint:", e)