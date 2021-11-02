from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Pet, ADOCAO


@admin.register(Pet)
class PetAdmin(LeafletGeoAdmin):
    """ Classe de registro de administrador pra cadastro de pets """
    list_display = ['id', 'nome','descricao','user','coordenada']


@admin.register(ADOCAO)
class AdocaoAdmin(admin.ModelAdmin):
    """ Classe de registro de administrador pra cadastro de adoção de pets """
    list_display = ['status', 'dataEntrada', 'dataAdocao',
                    'observacao','dataCriacao','dataModificacao']
