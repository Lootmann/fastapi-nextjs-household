from api.models import categories as category_model


def test_category_model_repr():
    category = category_model.Category(id=1, name="grocery", households=[], user_id=1)
    assert (
        str(category)
        == f"<Category (id, name, user_id) = ({category.id}, {category.name}, {category.user_id})>"
    )
