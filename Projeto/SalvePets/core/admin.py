from django.contrib import admin
from .models import Pet
from leaflet.admin import LeafletGeoAdmin

# Register your models here.
@admin.register(Pet)
class PetAdmin(LeafletGeoAdmin):        #admin.ModelAdmin
    list_display = ['id', 'nome','descricao','user','coordenada']

