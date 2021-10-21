from decimal import Decimal

import pytest

from ..models import Item, Order

pytestmark = pytest.mark.django_db


def test___str__(product):
    order = Order.objects.create(
        cpf="401.142.450-10",
        name="Fulano",
        email="test@fulano.com",
        postal_code="76900-649",
        address="Rua Castro Alves",
        number="123",
        district="Jardim dos Migrantes",
        state="RO",
        city="Ji-Paraná",
    )
    assert order.__str__() == f"Pedido {order.id}"
    assert str(order) == f"Pedido {order.id}"

    item = Item.objects.create(
        order=order,
        product=product,
        price=Decimal(10),
        quantity=1,
    )

    assert item.__str__() == str(item.id)
    assert str(item) == str(item.id)