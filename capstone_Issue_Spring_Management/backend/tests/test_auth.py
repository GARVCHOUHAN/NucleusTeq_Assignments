"""
Authentication API tests.
"""

from app.database.collections import users_collection


REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"


def test_register_user_success(client):
    """
    Test successful registration.
    """

    response = client.post(
        REGISTER_URL,
        json={
            "name": "Garv",
            "email": "garv@test.com",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )

    assert response.status_code == 201

    assert response.json() == {
        "message": "User registered successfully."
    }


def test_register_duplicate_email(client):
    """
    Duplicate email should fail.
    """

    payload = {
        "name": "Garv",
        "email": "garv@test.com",
        "password": "Password@123",
        "role": "MEMBER"
    }

    client.post(
        REGISTER_URL,
        json=payload
    )

    response = client.post(
        REGISTER_URL,
        json=payload
    )

    assert response.status_code == 409

    assert response.json()["detail"] == "Email already registered."


def test_register_invalid_email(client):
    """
    Invalid email validation.
    """

    response = client.post(
        REGISTER_URL,
        json={
            "name": "Garv",
            "email": "abc",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )

    assert response.status_code == 422


def test_register_short_password(client):
    """
    Password length validation.
    """

    response = client.post(
        REGISTER_URL,
        json={
            "name": "Garv",
            "email": "garv@test.com",
            "password": "123",
            "role": "MEMBER"
        }
    )

    assert response.status_code == 422


def test_password_is_hashed(client):
    """
    Ensure password is not stored
    in plain text.
    """

    client.post(
        REGISTER_URL,
        json={
            "name": "Garv",
            "email": "garv@test.com",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )

    user = users_collection.find_one(
        {
            "email": "garv@test.com"
        }
    )

    assert user is not None

    assert user["password"] != "Password@123"


def test_login_success(client):
    """
    Successful login.
    """

    client.post(
        REGISTER_URL,
        json={
            "name": "Garv",
            "email": "garv@test.com",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )

    response = client.post(
        LOGIN_URL,
        json={
            "email": "garv@test.com",
            "password": "Password@123"
        }
    )

    assert response.status_code == 200

    assert response.json()["message"] == "Login successful."


def test_login_wrong_password(client):
    """
    Invalid password.
    """

    client.post(
        REGISTER_URL,
        json={
            "name": "Garv",
            "email": "garv@test.com",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )

    response = client.post(
        LOGIN_URL,
        json={
            "email": "garv@test.com",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid email or password."


def test_login_unknown_email(client):
    """
    Unknown email.
    """

    response = client.post(
        LOGIN_URL,
        json={
            "email": "unknown@test.com",
            "password": "Password@123"
        }
    )

    assert response.status_code == 401


def test_login_empty_body(client):
    """
    Missing fields.
    """

    response = client.post(
        LOGIN_URL,
        json={}
    )

    assert response.status_code == 422


def test_role_saved_correctly(client):
    """
    Verify role is stored.
    """

    client.post(
        REGISTER_URL,
        json={
            "name": "Admin",
            "email": "admin@test.com",
            "password": "Password@123",
            "role": "ADMIN"
        }
    )

    user = users_collection.find_one(
        {
            "email": "admin@test.com"
        }
    )

    assert user["role"] == "ADMIN"
    
    
def test_register_missing_name(client):

    response = client.post(
        "/auth/register",
        json={
            "email": "garv@test.com",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )

    assert response.status_code == 422

def test_register_missing_email(client):

    response = client.post(
        "/auth/register",
        json={
            "name": "Garv",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )

    assert response.status_code == 422

def test_register_missing_password(client):

    response = client.post(
        "/auth/register",
        json={
            "name": "Garv",
            "email": "garv@test.com",
            "role": "MEMBER"
        }
    )

    assert response.status_code == 422

def test_register_invalid_role(client):

    response = client.post(
        "/auth/register",
        json={
            "name": "Garv",
            "email": "garv@test.com",
            "password": "Password@123",
            "role": "CEO"
        }
    )

    assert response.status_code == 422
    
def test_register_name_too_short(client):

    response = client.post(
        "/auth/register",
        json={
            "name": "A",
            "email": "garv@test.com",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )

    assert response.status_code == 422

def test_login_missing_password(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "garv@test.com"
        }
    )

    assert response.status_code == 422

def test_login_missing_email(client):

    response = client.post(
        "/auth/login",
        json={
            "password": "Password@123"
        }
    )

    assert response.status_code == 422

from app.core.security import (
    hash_password,
    verify_password
)


def test_password_hash_verification():

    password = "Password@123"

    hashed_password = hash_password(password)

    assert verify_password(
        password,
        hashed_password
    )

def test_invalid_password_hash():

    hashed_password = hash_password(
        "Password@123"
    )

    assert not verify_password(
        "WrongPassword",
        hashed_password
    )

def test_login_does_not_return_password(client):

    client.post(
        "/auth/register",
        json={
            "name": "Garv",
            "email": "garv@test.com",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "garv@test.com",
            "password": "Password@123"
        }
    )

    assert "password" not in response.json()["user"]