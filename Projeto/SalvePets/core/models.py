from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Value
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

# from django.contrib.gis.db import models ////CORRIGIR

# Create your models here.

"""
    SEXO_CHOICES = (
        ('M', u'Masculino'),
        ('F', u'Feminino'),
    )

    ESTADO_CIVIL_CHOICES = (
        ('S', u'Solteiro'),
        ('C', u'Casado'),
        ('D', u'Divorciado'),
        ('V', u'Viúvo'),
    )
"""
"""
class TiposUsuario(models.IntegerChoices):
    US_NORMAL = 0, 'normal'
    US_EMPRESA = 1, 'empresa'
    US_INSTITUICAO = 2, 'instituição'
"""
PET_CHOICES = (
    ('perdido','PERDIDO'),
    ('encontrado','ENCONTRADO'),
)

class LOCALIZACAO(models.Model):
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    rua = models.CharField(max_length=200)
    cep = models.CharField(max_length=10)
    num = models.IntegerField()
    bairro = models.CharField(max_length=50)
    # coordenada = models.PointField() ///// CORRIGIR

class USUARIO(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    FK_idLocalizacao = models.ForeignKey(LOCALIZACAO, on_delete=models.RESTRICT)
   # tipoUsuario = models.IntegerField(choices=TiposUsuario.choices)
    nome = models.CharField(max_length=100)
    cpfCnpj = models.CharField(max_length=11, blank=True, null=True)
    dataNascimento = models.DateField(default=timezone.now, blank=True, null=True)
    telefone = models.CharField(max_length=11, blank=True, null=True, verbose_name='Nº telefone')
    pontuacao = models.DecimalField(max_digits=30, decimal_places=15)

class ABRIGO(models.Model):
    FK_idUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    FK_idLocalizacao = models.ForeignKey(LOCALIZACAO, on_delete=models.RESTRICT)
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #FK_idAbrigo = models.ForeignKey(ABRIGO, on_delete=models.RESTRICT)      #precisa remover a FK abrigo
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    observacoes = models.TextField()
    comprimento = models.DecimalField(max_digits=30, decimal_places=15)
    largura = models.DecimalField(max_digits=30, decimal_places=15)
    dataNascimento = models.DateField(blank=True, null=True)
    raca = models.CharField(max_length=50)
    cor = models.CharField(max_length=30)
    altura = models.DecimalField(max_digits=30, decimal_places=15)
    peso = models.DecimalField(max_digits=30, decimal_places=15)
    ativo = models.BooleanField(default=True)                                                             #campo add
    encontradoPerdido = models.CharField(max_length=10, choices=PET_CHOICES, default='encontrado')  #campo add
    foto = models.ImageField(upload_to='pet')                #(upload_to='<caminho a ser salvo>')                  #campo add

class PET_PERDIDO_ENCONTRADO(models.Model):
    FK_idPet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    FK_idLocalizacao = models.ForeignKey(LOCALIZACAO, on_delete=models.RESTRICT)
    observacoes = models.TextField()
    status = models.CharField(max_length=20)
    data = models.DateField(blank=True, null=True)

class PATROCINIO(models.Model):
    FK_idUsuario = models.ManyToManyField(User)
    FK_idPet = models.ForeignKey(Pet, on_delete=models.RESTRICT)
    observacoes = models.TextField()
    valor = models.DecimalField(max_digits=30, decimal_places=15)
    data = models.DateField(blank=True, null=True)

class ADOCAO(models.Model):
    FK_idPet = models.ForeignKey(Pet, on_delete=models.RESTRICT)
    FK_idUsuario =  models.ForeignKey(User, on_delete=models.RESTRICT)
    status = models.CharField(max_length=20)
    dataEntrada = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    dataAdocao = models.DateTimeField(blank=True, null=True)
    observacao = models.TextField()

class TOKEN(models.Model):
    FK_idUsuario =  models.ForeignKey(User, on_delete=models.CASCADE)
    dataToken = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=20)

class ANUNCIO(models.Model):
    FK_idUsuario =  models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    observacoes = models.TextField()
    tipo = models.CharField(max_length=50)
    dataInicio = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    dataFim = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=30, decimal_places=15)

class OPCAO_ENTREGA(models.Model):
    opcaoEntrega = models.CharField(max_length=50)
    prazoEntrega = models.IntegerField()
    frete = models.DecimalField(max_digits=30, decimal_places=15)

class FORMA_PAGAMENTO(models.Model):
    formaPagamento = models.CharField(max_length=50)

class PRODUTO(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    dadosTecnicos = models.TextField()
    valor = models.DecimalField(max_digits=30, decimal_places=15)
    categoria = models.CharField(max_length=100)

class PEDIDO(models.Model):
    FK_idUsuario =  models.ForeignKey(User, on_delete=models.CASCADE)
    FK_idProduto = models.ManyToManyField(PRODUTO)
    FK_idOpcaoEntrega = models.ForeignKey(OPCAO_ENTREGA, on_delete=models.RESTRICT)
    FK_idFormaPagamento = models.ForeignKey(FORMA_PAGAMENTO, on_delete=models.RESTRICT)
    FK_idLocalizacao = models.ForeignKey(LOCALIZACAO, on_delete=models.RESTRICT)
    desconto = models.DecimalField(max_digits=30, decimal_places=15)
    status = models.CharField(max_length=50)

class AVALIACAO(models.Model):
    FK_idUsuario = models.ManyToManyField(User)
    nota = models.DecimalField(max_digits=30, decimal_places=15)
    comentario = models.TextField()