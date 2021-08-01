from django.contrib import admin
from .models import Pet
from leaflet.admin import LeafletGeoAdmin

@admin.register(Pet)
class PetAdmin(LeafletGeoAdmin):
    list_display = ['id', 'nome','descricao','user','coordenada']

