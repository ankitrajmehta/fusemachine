import pytest
import requests
import asyncio

ENDPOINT = "http://localhost:8000/messages"

# Check if app exists
def test_app_exists():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

# Check if sentiment is calculated correctly
def test_create_message_and_calculate_sentiment():
    payload = {
            "user_message": "test message with no sentinment",
            "timestamp": "2025-05-14T12:00:00Z",
            "replied": False
            }
    response = requests.post(ENDPOINT, json=payload)
    assert response.status_code == 200
    assert -1 <= float(response.json()['sentinment']) <= 1

# Check if the bot message is happy
def test_create_message_happy():
    payload = {
            "user_message": "i am very sad",
            "timestamp": "2025-05-14T12:00:00Z",
            "replied": False
            }
    response = requests.post(ENDPOINT + "/happy", json=payload)
    assert response.status_code == 200
    assert response.json()['bot_message'] is not None
    payload["user_message"] = response.json()['bot_message']
    assert float(requests.post(ENDPOINT, json= payload).json()['sentinment']) > 0

# Check if the bot message is sad
def test_create_message_sad():
    payload = {
            "user_message": "i am very happy",
            "timestamp": "2025-05-14T12:00:00Z",
            "replied": False
            }
    response = requests.post(ENDPOINT + "/sad", json=payload)
    assert response.status_code == 200
    assert response.json()['bot_message'] is not None
    payload["user_message"] = response.json()['bot_message']
    assert float(requests.post(ENDPOINT, json= payload).json()['sentinment']) < 0
