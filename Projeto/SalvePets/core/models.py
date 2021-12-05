from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from localflavor.br.models import BRCPFField, BRPostalCodeField, BRStateField, BRCNPJField

# ------------------ testes --------------
class Post(models.Model):
    body = models.TextField()

# ===       Escolhas       ===

TIPOS_USUARIO = (
    ('Usuário comum', _('Usuário comum')),
    ('Instituição', _('Instituição')),
)

PET_CHOICES = (
    (_("Perdido"),_("PERDIDO")),
    (_("Encontrado"),_("ENCONTRADO")),
)

ESPECIE = (
    ("Cachorro",_("Cachorro")),
    ("Gato",_("Gato")),
    ("Outros",_("Outros")),
)

SEXO = (
    ("Macho",_("Macho")),
    ("Fêmea",_("Fêmea")),
    ("Não sei",_("Não sei")),
)
# ============================

# ===       Tabelas        ===

class INSTITUICAO(models.Model):
    """ Modelo de dados de instituição """
    ativo = models.BooleanField(default=True, blank=False, null=False)
    nome_instituicao = models.CharField(max_length=50, null=True)
    razao_social = models.CharField(max_length=50, null=True)
    cnpj=BRCNPJField("CNPJ", null=True)
    telefone = models.CharField(max_length=25, null=True)
    email = models.CharField(max_length=50, null=True)
    postal_code = BRPostalCodeField("CEP")
    address = models.CharField("Endereço", max_length=250)
    number = models.CharField("Número", max_length=250)
    complement = models.CharField("Complemento", max_length=250, blank=True)
    district = models.CharField("Bairro", max_length=250)
    state = BRStateField("Estado")
    city = models.CharField("Cidade", max_length=250)

    doacao_valor_20_link = models.CharField(_("R$ 20"), max_length=250, null = True, blank = True)
    doacao_valor_50_link = models.CharField(_("R$ 50"), max_length=250, null = True, blank = True)
    doacao_valor_100_link = models.CharField(_("R$ 100"), max_length=250, null = True, blank = True)

    doacao_limpeza_link = models.CharField(_("Link para ajudar com limpeza"), max_length=250, null = True, blank = True)
    doacao_limpeza_valor = models.DecimalField(_("Valor da limpeza"), max_digits=6, decimal_places=2, null = True, blank = True)

    doacao_alimentacao_link = models.CharField(_("Link para ajudar com alimentação"), max_length=250, null = True, blank = True)
    doacao_alimentacao_valor = models.DecimalField(_("Valor da alimentação"), max_digits=6, decimal_places=2, null = True, blank = True)

    doacao_medicamentos_link = models.CharField(_("Link para ajudar com medicamentos"), max_length=250, null = True, blank = True)
    doacao_medicamentos_valor = models.DecimalField(_("Valor dos medicamentos"), max_digits=6, decimal_places=2, null = True, blank = True)

    doacao_diaria_internacao_link = models.CharField(_("Link para ajudar com diária de internação"), max_length=250, null = True, blank = True)
    doacao_diaria_internacao_valor = models.DecimalField(_("Valor da diária de internação"), max_digits=6, decimal_places=2, null = True, blank = True)
    
    doacao_patrocinio_codigo = models.CharField(_("Código do patrocínio"), max_length=250, null = True, blank = True)
    doacao_patrocinio_valor = models.DecimalField(_("Valor do patrocínio"), max_digits=6, decimal_places=2, null = True, blank = True)


class AVALIACAO(models.Model):
    """ Modelo de dados de avaliação """
    fk_id_instituicao = models.ForeignKey(INSTITUICAO, on_delete=models.SET_NULL, null=True)
    fk_id_avaliador = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    nota = models.IntegerField(blank=True, null=True)
    #nota_geral = models.IntegerField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    #dataModificacao = models.DateTimeField(auto_now=True)


class USUARIO(models.Model):
    """ Modelo de dados de usuário """
    user = models.OneToOneField(User, on_delete=CASCADE)
    tipousuario = models.CharField(max_length=30, choices=TIPOS_USUARIO, default='Usuário comum',
                                   verbose_name=_("Tipo de usuário"), blank=False, null=False)
    #cpfcnpj = models.CharField(max_length=14, verbose_name=_("CPF (somente números)"), blank=False,null=False)
    cpfcnpj = BRCPFField("CPF")
    dataNascimento = models.DateField(verbose_name=_("Data de nascimento"), blank=True, null=True)
    telefone = models.CharField(max_length=25,
                                verbose_name=_("Número de celular (somente números)"), blank=True,
                                null=True)
    pontuacao = models.DecimalField(max_digits=30, decimal_places=15, blank=True, null=True)
    receberNotificacoes = models.BooleanField(default=True,
                                              verbose_name=_("Receber notificações"), blank=False,
                                              null=False)
    site = models.CharField(max_length=100, verbose_name=_("Site"), blank=True, null=True)
    idImagem = models.ImageField(upload_to='usuario', blank=True, null=True)
    dataCriacao = models.DateTimeField(auto_now_add=True, null=True)
    dataModificacao = models.DateTimeField(auto_now=True, null=True)
    fk_instituicao = models.ForeignKey(INSTITUICAO, on_delete=models.SET_NULL, null=True)
    is_admin_instituicao=models.BooleanField(default=False, blank=False, null=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        USUARIO.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.usuario.save()

class Pet(models.Model):
    """ Modelo de dados de pet """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_id_instituicao = models.ForeignKey(INSTITUICAO, on_delete=models.SET_NULL, blank=True,
                                          null=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    dataPerdaEncontro = models.DateField(blank=True, null=True)
    especie = models.CharField(max_length=50, choices=ESPECIE, default="Cachorro",
                               verbose_name=_("Espécie"), blank=False, null=False)
    raca = models.CharField(max_length=50, blank=True, null=True)
    cor = models.CharField(max_length=30, blank=True, null=True)
    porte = models.IntegerField(default=80, verbose_name=_("Porte"), blank=False, null=False)
    ativo = models.BooleanField(default=True, blank=True, null=True)
    adotado = models.BooleanField(default=False, blank=True, null=True)
    encontradoPerdido = models.CharField(max_length=10, choices=PET_CHOICES, blank=True, null=True)
    foto = models.ImageField(upload_to='pet', blank=False, null=False)
    coordenada = models.PointField(srid=4326, blank=True, null=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)
    sexo = models.CharField(max_length=20, choices=SEXO, default="Macho", verbose_name=_("Sexo"),
                            blank=True, null=True)
    dataNascimento = models.DateField(blank=True, null=True)
    fk_id_usuario_adocao = models.ForeignKey(USUARIO, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.nome}'

class PATROCINIO(models.Model):
    """ Modelo de dados de patrocínio """
    FK_idUsuario = models.ManyToManyField(User)
    FK_idPet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null= True)
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    data = models.DateField(blank=True, null=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)
    publico = models.BooleanField(default=True, blank=False, null= False)
    pago = models.BooleanField(default=False, blank=False, null= False)

    doacao_tipo = models.CharField(_("Tipo de doação"), max_length=50, null=False, default = "doacao")

    class Meta:
        ordering = ['data']

class ADOCAO(models.Model):
    """ Modelo de dados de adoção """
    FK_idPet = models.ForeignKey(Pet, on_delete=models.RESTRICT)
    FK_idUsuario = models.ForeignKey(User, on_delete=models.RESTRICT)
    status = models.CharField(max_length=20)
    dataEntrada = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    dataAdocao = models.DateTimeField(blank=True, null=True)
    observacao = models.TextField()
    dataCriacao = models.DateTimeField(auto_now_add=True)
    dataModificacao = models.DateTimeField(auto_now=True)
