from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
# from django.contrib.gis.db import models ////CORRIGIR

# Create your models here.

class LOCALIZACAO(models.Model):
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    rua = models.CharField(max_length=200)
    cep = models.CharField(max_length=10)
    num = models.IntegerField()
    bairro = models.CharField(max_length=50)
    # coordenada = models.PointField() ///// CORRIGIR

class ABRIGO(models.Model):
    FK_idUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    FK_idLocalizacao = models.ForeignKey(LOCALIZACAO, on_delete=models.RESTRICT)
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    FK_idAbrigo = models.ForeignKey(ABRIGO, on_delete=models.RESTRICT)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    observacoes = models.TextField()
    comprimento = models.DecimalField(decimal_places=2,max_digits=3)
    largura = models.DecimalField(decimal_places=2,max_digits=3)
    dataNascimento = models.DateField()
    raca = models.CharField(max_length=50)
    cor = models.CharField(max_length=30)
    altura = models.DecimalField(decimal_places=2,max_digits=2)
    peso = models.DecimalField(decimal_places=2,max_digits=3)

    def __str__(self):
        return str(self.id)

    
