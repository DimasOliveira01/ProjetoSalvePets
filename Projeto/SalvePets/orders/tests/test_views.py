import pytest
from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed

pytestmark = pytest.mark.django_db


def test_reverse_resolve():
    assert reverse("orders:create") == "/orders/create/"
    assert resolve("/orders/create/").view_name == "orders:create"


def test_status_code(client):
    response = client.get(reverse("orders:create"))
    assert response.status_code == 200


def test_order_create_form_valid(client, product):
    form_data = {
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

    response = client.post(reverse("orders:create"), data=form_data, follow=True)
    assertTemplateUsed(response, "index.html")

    client.post(
        reverse("cart:add", kwargs={"product_id": product.id}),
        data={"quantity": 1, "override": False},
    )

    response = client.post(reverse("orders:create"), form_data, follow=True)
    assertTemplateUsed(response, "orders/order_created.html")