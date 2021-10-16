import pytest
from django.conf import settings
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


class TestCartAddView:
    def test_reverse_resolve(self, product):
        assert (
            reverse("cart:add", kwargs={"product_id": product.id})
            == f"/cart/add/{product.id}/"
        )
        assert resolve(f"/cart/add/{product.id}/").view_name == "cart:add"

    def test_add_product_to_cart(self, client, product):
        response = client.post(
            reverse("cart:add", kwargs={"product_id": product.id}),
            data={"quantity": 1, "override": False},
        )
        assert response.status_code == 302
        assert response.url == "/cart/"
        assert str(product.id) in client.session[settings.CART_SESSION_ID]


class TestCartRemoveView:
    def test_reverse_resolve(self, product):
        assert (
            reverse("cart:remove", kwargs={"product_id": product.id})
            == f"/cart/remove/{product.id}/"
        )
        assert resolve(f"/cart/remove/{product.id}/").view_name == "cart:remove"

    def test_remove_product_from_cart(self, client, product):
        client.post(
            reverse("cart:add", kwargs={"product_id": product.id}),
            data={"quantity": 1, "override": False},
        )

        response = client.post(
            reverse("cart:remove", kwargs={"product_id": product.id})
        )

        assert response.status_code == 302
        assert response.url == "/cart/"
        assert str(product.id) not in client.session[settings.CART_SESSION_ID]


class TestCartDetailView:
    def test_reverse_resolve(self, product):
        assert reverse("cart:detail") == "/cart/"
        assert resolve("/cart/").view_name == "cart:detail"

    def test_status_code(self, client):
        response = client.get(reverse("cart:detail"))
        assert response.status_code == 200