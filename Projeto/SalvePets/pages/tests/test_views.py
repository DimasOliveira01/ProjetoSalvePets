import pytest
from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.fixture
def home_response(client):
    return client.get(reverse("pages:home_ecommerce"))


#@pytest.fixture
#def about_response(client):
#    return client.get(reverse("pages:about"))


class TestHomePageView:
    def test_reverse_resolve(self):
        assert reverse("pages:home_ecommerce") == "/ecommerce/"
        assert resolve("/ecommerce/").view_name == "pages:home_ecommerce"

    def test_status_code(self, home_response):
        assert home_response.status_code == 200

    def test_template(self, home_response):
        assertTemplateUsed(home_response, "products/product_list.html")


#class TestAboutView:
#    def test_reverse_resolve(self):
#        assert reverse("pages:about") == "/about/"
#        assert resolve("/about/").view_name == "pages:about"

#    def test_status_code(self, about_response):
#        assert about_response.status_code == 200

#    def test_template(self, about_response):
#        assertTemplateUsed(about_response, "about.html")

