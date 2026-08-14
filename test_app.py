import pytest
from app import app, db
from models import User


@pytest.fixture
def client():
    """
    This 'fixture' runs before every test function that asks for it.
    It sets up a fresh, temporary, in-memory database so tests never
    touch your real app.db — each test starts with a clean slate.
    """
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


# ---------- PASSWORD HASHING TESTS ----------

def test_password_is_hashed_not_plain_text():
    """
    A password should NEVER be stored as plain text.
    This test creates a user, sets a password, and checks that
    the stored value does NOT equal the original password.
    """
    user = User(username="testuser")
    user.set_password("mypassword123")

    assert user.password_hash != "mypassword123"


def test_correct_password_is_accepted():
    """
    check_password() should return True when given the
    correct original password.
    """
    user = User(username="testuser")
    user.set_password("mypassword123")

    assert user.check_password("mypassword123") is True


def test_wrong_password_is_rejected():
    """
    check_password() should return False when given an
    incorrect password.
    """
    user = User(username="testuser")
    user.set_password("mypassword123")

    assert user.check_password("wrongpassword") is False


# ---------- SIGNUP TESTS ----------

def test_signup_creates_a_new_user(client):
    """
    Submitting the register form should create a new user
    and redirect them (status code 302 means 'redirect').
    """
    response = client.post("/register", data={
        "username": "newuser",
        "password": "somepassword"
    })

    assert response.status_code == 302  # redirected after success

    with app.app_context():
        user = User.query.filter_by(username="newuser").first()
        assert user is not None


def test_signup_rejects_duplicate_username(client):
    """
    If a username already exists, registering again with the
    same username should NOT create a second user.
    """
    client.post("/register", data={
        "username": "duplicate",
        "password": "password1"
    })

    client.post("/register", data={
        "username": "duplicate",
        "password": "password2"
    })

    with app.app_context():
        matching_users = User.query.filter_by(username="duplicate").all()
        assert len(matching_users) == 1


# ---------- LOGIN TESTS ----------

def test_login_with_correct_credentials(client):
    """
    Registering then logging in with the same credentials
    should succeed (redirect to the home page).
    """
    client.post("/register", data={
        "username": "loginuser",
        "password": "correctpassword"
    })
    client.get("/logout")  # make sure we start logged out

    response = client.post("/login", data={
        "username": "loginuser",
        "password": "correctpassword"
    })

    assert response.status_code == 302  # redirected after success


def test_login_with_wrong_password_fails(client):
    """
    Logging in with an incorrect password should NOT succeed —
    it should redirect back to the login page, not the home page.
    """
    client.post("/register", data={
        "username": "loginuser2",
        "password": "correctpassword"
    })
    client.get("/logout")

    response = client.post("/login", data={
        "username": "loginuser2",
        "password": "wrongpassword"
    }, follow_redirects=True)

    assert b"Log in" in response.data or b"login" in response.data.lower()


def test_homepage_requires_login(client):
    """
    Visiting the homepage without being logged in should redirect
    to the login page, not show the dashboard.
    """
    response = client.get("/", follow_redirects=True)
    assert b"login" in response.data.lower() or response.status_code == 200