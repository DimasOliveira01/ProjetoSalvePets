import pytest
from django.urls import resolve, reverse
from pytest_django.asserts import assertTemplateUsed
from core import views

pytestmark = pytest.mark.django_db
"""
def test_reverse_resolve():
    assert reverse(views.lista_pets_encontrados) == "/lista-pet-encontrado/"
    assert resolve("/lista-pet-encontrado/").view_name == views.lista_pets_encontrados
"""
def test_status_code(client):
    response = client.get(reverse(views.lista_pets_encontrados))
    assert response.status_code == 200
"""
def test_reverse_resolve_index():
    assert reverse(views.index) == "/lista-pet-usuario"
    assert resolve("/lista-pet-usuario").view_name == views.index
"""
def test_index_form(client):
    response = client.post(reverse(views.index))
    assertTemplateUsed(response, "index.html")