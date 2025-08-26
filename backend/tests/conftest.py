# backend/tests/conftest.py
import pytest
from backend.app import create_app, db
from backend.app.models.user import User
from backend.app.models.roles import Role
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="session")
def app_ctx():
    """Create a Flask app with a fresh test database."""
    app = create_app("testing")

    with app.app_context():
        db.create_all()

        # Seed roles
        admin_role = Role(role_name="admin")
        user_role = Role(role_name="user")
        db.session.add_all([admin_role, user_role])
        db.session.commit()

        # Seed users with hashed passwords
        admin = User(
            email="admin@example.com",
            password_hash=generate_password_hash("Admin123!"),
            role=admin_role
        )

        user = User(
            email="alice@example.com",
            password_hash=generate_password_hash("User123!"),
            role=user_role
        )

        db.session.add_all([admin, user])
        db.session.commit()

        yield app   

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app_ctx):
    """Flask test client."""
    return app_ctx.test_client()


@pytest.fixture
def get_user():
    """Helper to fetch a fresh user object by email."""
    def _get_user(email):
        return User.query.filter_by(email=email).first()
    return _get_user


@pytest.fixture
def login_and_get_tokens():
    """
    Helper to log in a user and return JWT tokens.
    Returns (access_token, refresh_token, csrf_token)
    """
    def _login(client, email, password):
        response = client.post(
            "/auth/login",
            json={"email": email, "password": password},
        )
        assert response.status_code == 200

        data = response.get_json()
        access = data.get("access_token")
        refresh = data.get("refresh_token")

        # Extract CSRF token from cookies if present
        csrf_token = None
        if "csrf_access_token" in response.headers.get("Set-Cookie", ""):
            csrf_token = response.headers.get("Set-Cookie").split("csrf_access_token=")[1].split(";")[0]

        return access, refresh, csrf_token
    return _login


def get_csrf_from_client(client):
    """
    Fetch a CSRF token from the test client.
    Adjust this if your API exposes CSRF via cookies or endpoint.
    """
    resp = client.get("/auth/csrf")
    assert resp.status_code == 200
    cookie = resp.headers.get("Set-Cookie")
    csrf_token = cookie.split("csrf_token=")[1].split(";")[0]
    return csrf_token

@pytest.fixture
def app():
    app = create_app(test_config=True)
    with app.app_context():
        yield app
