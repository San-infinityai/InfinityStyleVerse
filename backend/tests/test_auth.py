# backend/tests/test_auth.py

import pytest
from werkzeug.security import check_password_hash
from backend.app.models.user import User

# Helper fixture to get a user from DB by email
@pytest.fixture
def get_user():
    def _get_user(email):
        return User.query.filter_by(email=email).first()
    return _get_user

# -------------------------
# Test registration route
# -------------------------
def test_register_success(client, app_ctx, get_user):
    """Test that a new user can register successfully"""
    # Push app context to ensure routes are registered
    with client.application.app_context():
        resp = client.post(
            "/auth/register",
            json={
                "name": "Bob",
                "email": "bob@example.com",
                "password": "Bob123!",
                "role": "user",
            },
            headers={"Content-Type": "application/json"},
        )

        assert resp.status_code == 201
        data = resp.get_json()
        assert data["msg"] == "User registered successfully"

        # Verify user exists in DB with hashed password
        user = get_user("bob@example.com")
        assert user is not None
        assert check_password_hash(user.password_hash, "Bob123!")

# -------------------------
# Test login and token generation
# -------------------------
def test_login_and_tokens(client, app_ctx, get_user, login_and_get_tokens):
    """Login as admin and verify access & refresh tokens"""
    with client.application.app_context():
        access, refresh, csrf = login_and_get_tokens(
            client, "admin@example.com", "Admin123!"
        )

        assert access is not None
        assert refresh is not None

        # Verify password hash in DB
        user = get_user("admin@example.com")
        assert user is not None
        assert user.password_hash != "Admin123!"
        assert check_password_hash(user.password_hash, "Admin123!")

# -------------------------
# Test refresh token flow
# -------------------------
def test_refresh_token_flow(client, app_ctx, get_user, login_and_get_tokens):
    """Test refresh token generates a new access token"""
    with client.application.app_context():
        access, refresh, csrf = login_and_get_tokens(
            client, "alice@example.com", "User123!"
        )

        resp = client.post(
            "/auth/refresh",
            headers={"Authorization": f"Bearer {refresh}"}
        )

        assert resp.status_code == 200
        new_access = resp.get_json().get("access_token")
        assert new_access is not None
        assert new_access != access
