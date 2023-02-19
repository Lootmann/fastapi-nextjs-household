from pprint import pprint as p

import pytest
from fastapi import status

from api.schemas import auths as auth_schema
from api.schemas import users as user_schema
from tests.factories import UserFactory
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestCreateToken:
    async def test_login_and_create_valid_token(self, client):
        # create user
        user: user_schema.UserCreateResponse = UserFactory.create_user()
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        assert resp.status_code == status.HTTP_201_CREATED

        # login using user
        resp = await client.post(
            "/login",
            data={"username": user.name, "password": user.password},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == status.HTTP_200_OK
