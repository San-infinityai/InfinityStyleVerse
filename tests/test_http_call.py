import pytest
import requests
from unittest.mock import patch, MagicMock
from backend.app.tasks.http_call import http_call_task, http_call


def mock_response(status=200, json_data=None, text_data=None, headers=None):
    """Helper to create a mock response object"""
    mock_resp = MagicMock()
    mock_resp.status_code = status
    mock_resp.headers = headers or {"content-type": "application/json"}
    if json_data is not None:
        mock_resp.json.return_value = json_data
    if text_data is not None:
        mock_resp.text = text_data
    return mock_resp


@patch("backend.app.tasks.http_call.allow", return_value=True)
@patch("backend.app.tasks.http_call.safe_request")
def test_http_call_allowed(mock_safe_request, mock_allow):
    """Test HTTP call allowed by rate limiter"""
    mock_safe_request.return_value = mock_response(json_data={"ok": True}, status=200)

    # run Celery task synchronously
    res = http_call_task.run("https://httpbin.org/get", "GET")

    assert res["status"] == 200
    assert isinstance(res["data"], dict)
    assert res["data"]["ok"] is True


@patch("backend.app.tasks.http_call.allow", return_value=False)
def test_http_call_blocked(mock_allow):
    """Test HTTP call blocked by rate limiter"""
    with pytest.raises(RuntimeError) as exc_info:
        http_call_task.run("https://httpbin.org/get", "GET")
    assert "Rate limit exceeded" in str(exc_info.value)


@patch("backend.app.tasks.http_call.allow", return_value=True)
@patch("backend.app.tasks.http_call.safe_request")
def test_http_call_request_exception(mock_safe_request, mock_allow):
    """Test HTTP call raises exception and triggers retry"""
    mock_safe_request.side_effect = requests.RequestException("fail")

    with pytest.raises(Exception) as exc_info:
        http_call_task.run("https://httpbin.org/get", "GET")

    assert "fail" in str(exc_info.value)


@patch("backend.app.utils.http_client.request")
def test_http_call_success(mock_http_client):
    """Test shared task wrapper for http_call"""
    mock_http_client.return_value = mock_response(json_data={"ok": True}, status=200)

    res = http_call("https://httpbin.org/get")
    assert res["status"] == 200
    assert res["data"]["ok"] is True
