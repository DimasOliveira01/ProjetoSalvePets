from django.contrib import admin
from .models import PATROCINIO, Pet, ADOCAO
from leaflet.admin import LeafletGeoAdmin

@admin.register(Pet)
class PetAdmin(LeafletGeoAdmin):
    list_display = ['id', 'nome','descricao','user','coordenada']


@admin.register(ADOCAO)
class AdocaoAdmin(admin.ModelAdmin):
    list_display = ['status', 'dataEntrada', 'dataAdocao','observacao','dataCriacao','dataModificacao']

@admin.register(PATROCINIO)
class PatrocinioAdmin(admin.ModelAdmin):
    list_display = ['FK_idPet', 'observacoes','valor','data','dataCriacao', 'dataModificacao', 'publico' , 'pago']