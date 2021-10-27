import pytest

from orders.tests.factories import ItemFactory, OrderFactory
from products.tests.factories import CategoryFactory, ProductFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def category():
    return CategoryFactory()


@pytest.fixture
def product():
    return ProductFactory()
    

@pytest.fixture
def order():
    return OrderFactory()


@pytest.fixture
def item():
    return ItemFactory()


@pytest.fixture
def order_form_data():
    return {
        "cpf": "401.142.450-10",
        "name": "Fulano",
        "email": "test@fulano.com",
        "postal_code": "76900-649",
        "address": "Rua Castro Alves",
        "number": "123",
        "district": "Jardim dos Migrantes",
        "state": "RO",
        "city": "Ji-Paraná",
    }