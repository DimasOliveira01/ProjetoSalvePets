from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pet(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    dataCadastro = models.DateTimeField(auto_now_add=True)
    #dataNascimento = models.DateField()
    raca = models.CharField(max_length = 100)
    cor = models.CharField(max_length = 100)
    #altura = models.FloatField()
    #peso = models.FloatField()
    #status = models.FloatField()
    foto = models.ImageField()
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.id)

    
