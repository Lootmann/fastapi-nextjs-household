from datetime import datetime
from random import randint

import pytest
from fastapi import status

from api.schemas import households as household_schema
from tests.factories import create_access_token
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetAllHouseholds:
    async def test_get_all_households_and_empty(self, client, login_fixture):
        _, headers = await login_fixture

        # get all
        resp = await client.get("/households", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

    async def test_get_all_households(self, client, login_fixture):
        _, headers = await login_fixture

        # create category
        resp = await client.post("/categories", json={"name": "hoge"}, headers=headers)
        category_id = resp.json()["id"]

        # create households
        current = datetime.now()
        for _ in range(10):
            await client.post(
                "/households",
                json={"amount": 1200, "registered_at": str(current), "category_id": category_id},
                headers=headers,
            )

        # get all
        resp = await client.get("/households", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 10


@pytest.mark.asyncio
class TestGetHousehold:
    async def test_get_household_by_id(self, client, login_fixture):
        _, headers = await login_fixture

        # create category
        resp = await client.post("/categories", json={"name": "hoge"}, headers=headers)
        category_id = resp.json()["id"]

        # create household
        resp = await client.post(
            "/households",
            json={"amount": 1200, "registered_at": str(datetime.now()), "category_id": category_id},
            headers=headers,
        )
        household_id = resp.json()["id"]

        # get by id
        resp = await client.get(f"/households/{household_id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        household = household_schema.Household(**resp.json())

        assert household.amount == 1200
        assert household.category_id == category_id
        assert household.id == household_id

    async def test_get_household_by_id_which_doesnt_exist(self, client, login_fixture):
        _, headers = await login_fixture

        # create household
        resp = await client.get(f"/households/123", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_household_find_by_category_name(self, client, login_fixture):
        _, headers = await login_fixture

        # create some categories
        category_names = ["grocery", "insurance", "salary"]
        category_ids = []

        for category_name in category_names:
            resp = await client.post(
                "/categories",
                json={"name": category_name},
                headers=headers,
            )
            category_ids.append(resp.json()["id"])

        num_of_categories = [randint(5, 10), randint(5, 10), randint(5, 10)]

        for idx, num in enumerate(num_of_categories):
            for _ in range(num):
                resp = await client.post(
                    "/households",
                    json={
                        "amount": randint(590, 2289),
                        "registered_at": str(datetime.now()),
                        "category_id": category_ids[idx],
                    },
                    headers=headers,
                )

        for idx, category_name in enumerate(category_names):
            resp = await client.get(
                f"/households/search?category_name={category_name}", headers=headers
            )
            assert resp.status_code == status.HTTP_200_OK
            assert len(resp.json()) == num_of_categories[idx]


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


@pytest.mark.asyncio
class TestUpdateHousehold:
    async def test_update_household(self, client, login_fixture):
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

        household_id = resp.json()["id"]

        # update household
        update_data = {
            "amount": 999999,
            "category_id": category_id,
        }
        resp = await client.patch(f"/households/{household_id}", json=update_data, headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        household = household_schema.Household(**resp.json())

        assert household.amount != 1200
        assert household.amount == 999999
        assert household.registered_at != current_date

        # update household with only amount
        update_data = {
            "amount": 10,
        }
        resp = await client.patch(f"/households/{household_id}", json=update_data, headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        household = household_schema.Household(**resp.json())

        assert household.amount != 999999
        assert household.amount == 10

        # update with only category_id
        update_data = {"category_id": 2}
        resp = await client.patch(f"/households/{household_id}", json=update_data, headers=headers)
        assert resp.json() == {"detail": "Category: 2 Not Found"}
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        resp = await client.post("/categories", json={"name": "new"}, headers=headers)
        category_id = resp.json()["id"]
        assert resp.status_code == status.HTTP_201_CREATED

        resp = await client.patch(f"/households/{household_id}", json=update_data, headers=headers)
        assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
class TestDeleteHousehold:
    async def test_delete_household(self, client, login_fixture):
        _, headers = await login_fixture

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
        household_id = resp.json()["id"]

        # delete household
        resp = await client.delete(f"/households/{household_id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

    async def test_delete_household_which_is_wrong(self, client, login_fixture):
        _, headers = await login_fixture

        # delete household
        resp = await client.delete("/households/1", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Household: 1 Not Found"}

    async def test_delete_household_trying_to_wrong_user(self, client, login_fixture):
        _, headers = await login_fixture

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
        household_id = resp.json()["id"]

        # create new user
        await client.post("/users", json={"name": "new user", "password": "dorwssap"})
        new_headers = await create_access_token(client, username="new user", password="dorwssap")

        # try to delete households
        resp = await client.delete(f"/households/{household_id}", headers=new_headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Wrong User"}
