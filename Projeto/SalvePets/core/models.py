from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

# ===       Escolhas       ===

TIPOS_USUARIO = (
    (1, _('Usuário comum')),
    (2, _('Instituição')),
)

PET_CHOICES = (
    (_("perdido"),_("PERDIDO")),
    (_("encontrado"),_("ENCONTRADO")),
)

PORTE = (
    (1,_("Pequeno porte")),
    (2,_("Médio porte")),
    (3,_("Grande porte")),
)
# ============================

# ===       Tabelas        ===

class LOCALIZACAO(models.Model):
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    rua = models.CharField(max_length=200)
    cep = models.CharField(max_length=10)
    num = models.IntegerField()
    bairro = models.CharField(max_length=50)
    # coordenada = models.PointField() ///// CORRIGIR
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

class USUARIO(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    #idImagem = models.ImageField(upload_to='media', null=True, blank=True)
    #FK_idLocalizacao = models.ForeignKey(LOCALIZACAO, on_delete=models.RESTRICT)
    tipoUsuario = models.IntegerField(choices=TIPOS_USUARIO, default=1, verbose_name=_("Tipo de usuário"), blank=False, null=False)
    cpfCnpj = models.CharField(max_length=11, verbose_name=_("CPF (somente números)"), blank=False, null=False)
    dataNascimento = models.DateField(verbose_name=_("Data de nascimento"), blank=True, null=True)
    telefone = models.CharField(max_length=11, verbose_name=_("Número de telefone (somente números)"), blank=True, null=True)
    pontuacao = models.DecimalField(max_digits=30, decimal_places=15, blank=True, null=True)
    receberNotificacoes = models.BooleanField(default=True, verbose_name=_("Receber notificações"), blank=False, null=False)
    site = models.CharField(max_length=100, verbose_name=_("Site"), blank=True, null=True)
    idImagem = models.ImageField(upload_to='usuario', blank=True, null=True)
    dataCriacao = models.DateTimeField(auto_now_add=True, null=True)
    dataModificacao = models.DateTimeField(auto_now=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        USUARIO.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.usuario.save()

class ABRIGO(models.Model):
    FK_idUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    FK_idLocalizacao = models.ForeignKey(LOCALIZACAO, on_delete=models.RESTRICT)
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #FK_idAbrigo = models.ForeignKey(ABRIGO, on_delete=models.RESTRICT)      #precisa remover a FK abrigo
    nome = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    dataNascimento = models.DateField(blank=True, null=True)
    raca = models.CharField(max_length=50, blank=True, null=True)
    cor = models.CharField(max_length=30, blank=True, null=True)
    porte = models.IntegerField(choices=PORTE, default=1, verbose_name=_("Porte"), blank=False, null=False)
    #peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ativo = models.BooleanField(default=True, blank=False, null=False)
    encontradoPerdido = models.CharField(max_length=10, choices=PET_CHOICES, default='encontrado', blank=False, null=False)
    foto = models.ImageField(upload_to='pet', blank=False, null=False)
    coordenada = models.PointField(default='POINT(-46.65647647383157, -23.561051152327074)', srid=4326, blank=False, null=False)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

class PET_PERDIDO_ENCONTRADO(models.Model):
    FK_idPet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    FK_idLocalizacao = models.ForeignKey(LOCALIZACAO, on_delete=models.RESTRICT)
    observacoes = models.TextField()
    status = models.CharField(max_length=20)
    data = models.DateField(blank=True, null=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

class PATROCINIO(models.Model):
    FK_idUsuario = models.ManyToManyField(User)
    FK_idPet = models.ForeignKey(Pet, on_delete=models.RESTRICT)
    observacoes = models.TextField()
    valor = models.DecimalField(max_digits=30, decimal_places=15)
    data = models.DateField(blank=True, null=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)    

class ADOCAO(models.Model):
    FK_idPet = models.ForeignKey(Pet, on_delete=models.RESTRICT)
    FK_idUsuario =  models.ForeignKey(User, on_delete=models.RESTRICT)
    status = models.CharField(max_length=20)
    dataEntrada = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    dataAdocao = models.DateTimeField(blank=True, null=True)
    observacao = models.TextField()
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

class TOKEN(models.Model):
    FK_idUsuario =  models.ForeignKey(User, on_delete=models.CASCADE)
    dataToken = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=20)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

class ANUNCIO(models.Model):
    FK_idUsuario =  models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    observacoes = models.TextField()
    tipo = models.CharField(max_length=50)
    dataInicio = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    dataFim = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=30, decimal_places=15)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

class OPCAO_ENTREGA(models.Model):
    opcaoEntrega = models.CharField(max_length=50)
    prazoEntrega = models.IntegerField()
    frete = models.DecimalField(max_digits=30, decimal_places=15)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

class FORMA_PAGAMENTO(models.Model):
    formaPagamento = models.CharField(max_length=50)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

class PRODUTO(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    dadosTecnicos = models.TextField()
    valor = models.DecimalField(max_digits=30, decimal_places=15)
    categoria = models.CharField(max_length=100)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

class PEDIDO(models.Model):
    FK_idUsuario =  models.ForeignKey(User, on_delete=models.CASCADE)
    FK_idProduto = models.ManyToManyField(PRODUTO)
    FK_idOpcaoEntrega = models.ForeignKey(OPCAO_ENTREGA, on_delete=models.RESTRICT)
    FK_idFormaPagamento = models.ForeignKey(FORMA_PAGAMENTO, on_delete=models.RESTRICT)
    FK_idLocalizacao = models.ForeignKey(LOCALIZACAO, on_delete=models.RESTRICT)
    desconto = models.DecimalField(max_digits=30, decimal_places=15)
    status = models.CharField(max_length=50)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

class AVALIACAO(models.Model):
    FK_idUsuario = models.ManyToManyField(User)
    nota = models.DecimalField(max_digits=30, decimal_places=15)
    comentario = models.TextField()
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)

# ============================