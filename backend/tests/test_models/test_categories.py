from api.models import categories as category_model


def test_category_model_repr():
    category = category_model.Category(id=1, name="grocery", households=[])
    assert str(category) == f"<Category (id, name) = ({category.id}, {category.name})>"
