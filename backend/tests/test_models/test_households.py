from datetime import datetime

from api.models import households as household_model


def test_household_model_repr():
    household = household_model.Household(
        id=1, amount=1000, registered_at=datetime.now(), category_id=1
    )
    assert (
        str(household)
        == f"<Household ({household.id}, {household.amount}, {household.registered_at})>"
    )
