from builtins import str
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user_model import User, UserRole
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token
from unittest.mock import patch


@pytest.mark.asyncio
async def test_create_user_access_denied(async_client, user_token, email_service):
    headers = {"Authorization": f"Bearer {user_token}"}

    user_data = {
        "nickname": generate_nickname(),
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }

    response = await async_client.post("/users/", json=user_data, headers=headers)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_retrieve_user_access_denied(async_client, verified_user, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get(f"/users/{verified_user.id}", headers=headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_retrieve_user_access_allowed(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(admin_user.id)


@pytest.mark.asyncio
async def test_update_user_email_access_denied(async_client, verified_user, user_token):
    updated_data = {"email": f"updated_{verified_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(
        f"/users/{verified_user.id}", json=updated_data, headers=headers
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_user_email_access_allowed(async_client, admin_user, admin_token):
    updated_data = {"email": f"updated_{admin_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        f"/users/{admin_user.id}", json=updated_data, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]


@pytest.mark.asyncio
async def test_delete_user(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(
        f"/users/{admin_user.id}", headers=headers
    )
    assert delete_response.status_code == 204

    fetch_response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert fetch_response.status_code == 404


@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client):
    user_data = {
        "email": "notanemail",
        "password": "ValidPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422


import pytest
from app.services.jwt_service import decode_token
from urllib.parse import urlencode


@pytest.mark.asyncio
async def test_login_success(async_client, verified_user):

    form_data = {"username": verified_user.email, "password": "MySuperPassword$1234"}
    response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    decoded_token = decode_token(data["access_token"])
    assert decoded_token is not None, "Failed to decode token"
    assert (
        decoded_token["role"] == "AUTHENTICATED"
    ), "The user role should be AUTHENTICATED"


@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    form_data = {
        "username": "nonexistentuser@here.edu",
        "password": "DoesNotMatter123!",
    }
    response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")


@pytest.mark.asyncio
async def test_login_incorrect_password(async_client, verified_user):
    form_data = {"username": verified_user.email, "password": "IncorrectPassword123!"}
    response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")


@pytest.mark.asyncio
async def test_login_unverified_user(async_client, unverified_user):
    form_data = {"username": unverified_user.email, "password": "MySuperPassword$1234"}
    response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_locked_user(async_client, locked_user):
    form_data = {"username": locked_user.email, "password": "MySuperPassword$1234"}
    response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
    assert (
        "Account locked due to too many failed login attempts."
        in response.json().get("detail", "")
    )


@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client, admin_token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(
        f"/users/{non_existent_user_id}", headers=headers
    )
    assert delete_response.status_code == 404


@pytest.mark.asyncio
async def test_update_user_github(async_client, admin_user, admin_token):
    updated_data = {"github_profile_url": "http://www.github.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        f"/users/{admin_user.id}", json=updated_data, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == updated_data["github_profile_url"]


@pytest.mark.asyncio
async def test_update_user_linkedin(async_client, admin_user, admin_token):
    updated_data = {"linkedin_profile_url": "http://www.linkedin.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        f"/users/{admin_user.id}", json=updated_data, headers=headers
    )
    assert response.status_code == 200
    assert (
        response.json()["linkedin_profile_url"] == updated_data["linkedin_profile_url"]
    )


@pytest.mark.asyncio
async def test_list_users_as_admin(async_client, admin_token):
    response = await async_client.get(
        "/users/", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert "items" in response.json()


@pytest.mark.asyncio
async def test_list_users_as_manager(async_client, manager_token):
    response = await async_client.get(
        "/users/", headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_users_unauthorized(async_client, user_token):
    response = await async_client.get(
        "/users/", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_user_duplicate_nickname(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    nickname = "TestUser123"

    user_data_1 = {
        "nickname": nickname,
        "email": "testuser1@example.com",
        "password": "SecurePassw0rd!",
        "role": "ADMIN",
    }

    user_data_2 = {
        "nickname": nickname,
        "email": "testuser2@example.com",
        "password": "SecurePassw0rd!",
        "role": "ADMIN",
    }

    # Mock the 'send_verification_email' method from the 'EmailService' class
    with patch(
        "app.services.email_service.EmailService.send_verification_email"
    ) as mock_send_email:
        mock_send_email.return_value = (
            None  # Assume sending email is successfully mocked
        )

        # Create the first user
        response = await async_client.post("/users/", json=user_data_1, headers=headers)
        assert response.status_code == 201, "Failed to create first user"

        # Attempt to create a second user with the same nickname
        response = await async_client.post("/users/", json=user_data_2, headers=headers)
        assert (
            response.status_code == 400
        ), "Did not handle duplicate nickname correctly"


from unittest.mock import patch
import pytest

@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    email = "test@example.com"
    user_data_1 = {
        "nickname": generate_nickname(),
        "email": email,
        "password": "sS#fdasrongPassword123!",
        "role": "ADMIN",
    }

    user_data_2 = {
        "nickname": generate_nickname(),
        "email": email,
        "password": "AnotherStrongPassword123!",
        "role": "ADMIN",
    }

    with patch("app.services.email_service.EmailService.send_verification_email") as mock_send_email:
        mock_send_email.return_value = None  # Assume sending email is successfully mocked

        # Create the first user
        response1 = await async_client.post("/users/", json=user_data_1, headers=headers)
        assert response1.status_code == 201, "Failed to create first user"

        # Attempt to create a second user with the same email
        response2 = await async_client.post("/users/", json=user_data_2, headers=headers)
        assert response2.status_code == 400, "Duplicate email should result in an error"

