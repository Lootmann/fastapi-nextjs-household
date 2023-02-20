import pytest

from api.models import users as user_model
from api.schemas import users as user_schema
from tests.factories import UserFactory, random_string
from tests.init_async_client import async_client as client


@pytest.fixture
@pytest.mark.asyncio
async def user_fixture(client):
    user = user_model.User(name=random_string(), password=random_string())
    resp = await client.post("/users", json={"name": user.name, "password": user.password})
    user.id = resp.json()["id"]
    return user
