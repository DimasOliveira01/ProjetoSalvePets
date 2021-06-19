#from django.db import models
from DjangoSalvePets.db import models

# Create your models here.

class Pet(models.model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()
    dataCadastro = models.DateTimeField(auto_now_add=True)
    dataNascimento = models.DateField()
    raca = models.CharField(max_length = 100)
    cor = models.CharField(max_length = 100)
    altura = models.float
    peso = models.float
    status = models.float


    def __str__(self):
        return str(self.id)

    class Meta:
        bd_table = 'pet'

