from datetime import datetime

import pytest
from fastapi import status

from api.schemas import categories as category_schema
from api.schemas import households as household_schema
from tests.factories import UserFactory, create_access_token, random_string
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetHousehold:
    async def test_get_all_households(self, client, login_fixture):
        user, headers = await login_fixture

        # get all
        resp = await client.get("/households", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0


@pytest.mark.asyncio
class TestPostHousehold:
    async def test_create_household(self, client, login_fixture):
        user, headers = await login_fixture

        # create category
        resp = await client.post("/categories", json={"name": "hoge"}, headers=headers)
        category_id = resp.json()["id"]

        # create households
        current_date = datetime.now()
        resp = await client.post(
            "/households",
            json={"amount": 1200, "registered_at": str(current_date), "category_id": category_id},
            headers=headers,
        )
        assert resp.status_code == status.HTTP_201_CREATED

        household = household_schema.HouseholdCreateResponse(**resp.json())

        assert household.user_id == user.id
        assert household.amount == 1200
        assert household.registered_at == current_date
        assert household.category_id == category_id
