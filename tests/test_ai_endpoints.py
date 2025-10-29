#Pytest setup for Day 6 AI endpoint tests
import requests
import pytest

# Base URLs for the endpoints (adjusted ports based on your mock routes)
BASE_URLS = {
    "predict": "http://localhost:5000/api/infinitybrain/predict",
    "recommend": "http://localhost:5000/api/personamesh/recommend",
    "intentlogic": "http://localhost:5001/api/intentlogic",  # <-- check port
}

@pytest.fixture(scope="module")
def setup_servers():
    """
    Ensure all mock Flask servers are running before tests.
    """
    yield  # No teardown needed for mock testing

@pytest.mark.parametrize("endpoint, payload, expected_keys", [
    ("predict", {"prompt": "Predict trend for winter"}, ["trend_forecast", "confidence"]),
    ("recommend", {"user_id": "user1"}, ["recommendation", "confidence"]),
    ("intentlogic", {"user_action": "viewed_dress"}, ["user_action", "intent_scores"])
])
def test_ai_endpoints(setup_servers, endpoint, payload, expected_keys):
    """
    Generic test for AI endpoints to verify:
    - HTTP status is 200
    - Expected keys exist in response JSON
    - Confidence and intent_scores values are within valid ranges
    """
    url = BASE_URLS[endpoint]
    response = requests.post(url, json=payload)

    assert response.status_code == 200, f"{endpoint} failed: {response.text}"

    data = response.json()
    assert all(key in data for key in expected_keys), f"{endpoint} missing keys: {data}"

    # Confidence value check
    if "confidence" in data:
        assert 0.7 <= float(data["confidence"]) <= 1.0, f"{endpoint} confidence out of range: {data['confidence']}"

    # Intent scores value check
    if "intent_scores" in data:
        assert all(0.5 <= float(v) <= 0.95 for v in data["intent_scores"].values()), \
               f"{endpoint} intent scores out of range: {data['intent_scores']}"
