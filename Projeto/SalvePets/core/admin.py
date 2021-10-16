from django.contrib import admin
from .models import Pet, ADOCAO
from leaflet.admin import LeafletGeoAdmin

@admin.register(Pet)
class PetAdmin(LeafletGeoAdmin):
    list_display = ['id', 'nome','descricao','user','coordenada']


@admin.register(ADOCAO)
class AdocaoAdmin(admin.ModelAdmin):
    list_display = ['status', 'dataEntrada', 'dataAdocao','observacao','dataCriacao','dataModificacao']