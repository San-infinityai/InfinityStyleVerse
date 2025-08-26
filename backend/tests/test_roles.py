def test_admin_route_requires_token(client, app_ctx):
    """Accessing admin route without token should fail"""
    resp = client.get("/admin/users")
    assert resp.status_code == 401  # unauthorized without token


def test_user_cannot_access_admin(client, app_ctx, get_user, login_and_get_tokens):
    """Regular user should not access admin routes"""
    alice = get_user("alice@example.com")
    assert alice is not None

    access, refresh, csrf = login_and_get_tokens(client, "alice@example.com", "User123!")

    resp = client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {access}", "X-CSRFToken": csrf}
    )
    assert resp.status_code in (403, 401)  # forbidden or unauthorized


def test_admin_can_access_dashboard(client, app_ctx, get_user, login_and_get_tokens):
    """Admin user can access admin routes"""
    admin = get_user("admin@example.com")
    assert admin is not None

    access, refresh, csrf = login_and_get_tokens(client, "admin@example.com", "Admin123!")

    resp = client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {access}", "X-CSRFToken": csrf}
    )
    assert resp.status_code == 200
