# backend/tests/test_integration.py

import pytest

def test_login_then_access_admin_dashboard(client, app_ctx, get_user, login_and_get_tokens):
    """Login as admin and access admin dashboard"""
    
    # Ensure admin exists
    admin = get_user("admin@example.com")
    assert admin is not None

    # Correct fixture usage: inject login_and_get_tokens
    access, refresh, csrf = login_and_get_tokens(client, "admin@example.com", "Admin123!")

    headers = {"Authorization": f"Bearer {access}"}

    # Make request to an existing admin route
    resp = client.get("/admin/users", headers=headers)  # change to /admin/users or any existing admin route
    assert resp.status_code == 200

    # Optional: check response data
    data = resp.get_json()
    assert isinstance(data, list)
