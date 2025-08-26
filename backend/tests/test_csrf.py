# backend/tests/test_integration.py
def test_login_then_access_admin_dashboard(client, app_ctx, get_user, login_and_get_tokens):
    """Login as admin and access admin route"""
    admin = get_user("admin@example.com")
    assert admin is not None

    # Use fixture properly by passing it as an argument
    access, refresh, csrf = login_and_get_tokens(client, "admin@example.com", "Admin123!") 
    headers = {"Authorization": f"Bearer {access}", "X-CSRFToken": csrf}

    # Hit an existing admin route
    resp = client.get("/admin/users", headers=headers)
    assert resp.status_code == 200
