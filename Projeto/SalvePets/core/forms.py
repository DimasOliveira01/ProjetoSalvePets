from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import CharField
from django.forms.forms import Form
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Fieldset, Layout, Submit
from .models import Pet, USUARIO, ADOCAO, INSTITUICAO
import re
#from .custom_form_fields import cpfcnpjField, TelefoneField




# Criar Array de Ano de Nascimento - não sei se faz sentido mover pra arquivo separado..

BIRTH_YEAR_CHOICES  = []
for i in range(1900,2021):
    BIRTH_YEAR_CHOICES.append(str(i))

class SignupForm(forms.Form):
    """ Formulário de login """
    first_name = forms.CharField(max_length=30, label=_('Nome:'))
    last_name = forms.CharField(max_length=30, label=_('Sobrenome'))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

class PetForm(forms.ModelForm):
    """ Formulário de pet """
    class Meta:
        model = Pet
        fields = '__all__'



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class UsuarioForm(forms.ModelForm):
    """ Formulário de inclusão de usuário """
    #cpfcnpj = CpfcnpjField(label='CPF')
    '''dataNascimento = forms.DateField(required=True,
    widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),input_formats=['%d/%m/%Y','%m/%d/%Y'],
    label=_('Data de Nascimento'))'''
    dataNascimento = forms.DateField(required=True,
                                     widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
                                     label=_('Data de Nascimento'))
    telefone = forms.CharField(required=True, label=_('Número de Celular'))
    '''receberNotificacoes = forms.BooleanField(required=False,
    label = 'Desejo receber notificações', help_text='(Marque este campo caso deseje ser
    notificado sobre pets perdidos ou encontrados.)')'''
    class Meta:
        model = USUARIO
        #Retirei tipoUsuario
        fields = ('cpfcnpj', 'dataNascimento', 'telefone', 'site', 'receberNotificacoes')


class ExtendedSignupForm(SignupForm):
    """ Classe que seria usada como "Cadastro Único" - li que é possível fazer funcionar,
só preciso entender melhor como. Por enquanto não está implementada no Settings,
então não é utilizada """
    cpfcnpj = forms.CharField(max_length=14, label='CPF')
    '''dataNascimento = forms.DateField(required=True,
    widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),input_formats=['%d/%m/%Y'],
    label=_('Data de Nascimento'))'''
    dataNascimento = forms.DateField(required=True,
                                     widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
                                     label=_('Data de Nascimento'))
    telefone = forms.CharField(required=False, max_length=16, label=_('Número de Telefone'))
    receberNotificacoes = forms.BooleanField(required=False, label =
                                             _('Desejo receber notificações'),
                                             help_text=_('(Marque este campo caso deseje ser'+
                                             'notificado sobre pets perdidos ou encontrados.)'))
    #siteUrl = forms.URLField(initial='http://', label='URL do seu Site')





#Projeto integrado II
class ContactForm(forms.Form):
    """ Formulário de endereço """
    nome_fantasia = forms.CharField(max_length = 50)
    razao_social = forms.CharField(max_length = 50)
    numero_cnpj = forms.CharField(max_length = 18)
    numero_telefone = forms.CharField(max_length = 16)
    email_address = forms.EmailField(max_length = 150)


class AdocaoForm(forms.ModelForm):
    """ Formulário de adoção """
    class Meta:
        model = ADOCAO
        fields = '__all__'

class InstituicaoForm(forms.ModelForm):
    """ Formulário de cadastro de instituição """
    class Meta:
        model = INSTITUICAO
        fields = [
            'nome_instituicao',
            'razao_social',
            'cnpj',
            'telefone',
            'email',
            'postal_code',
            'address',
            'number',
            'complement',
            'district',
            'state',
            'city',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "."
        self.helper.add_input(
            Submit(
                "submit",
                "Atualizar",
                css_class="btn btn-outline-dark",
            )
        )
        self.helper.layout = Layout(
            Fieldset(
                "",
                "cnpj",
                "nome_instituicao",
                "razao_social",
                "telefone",
                "email",
                Div(
                    Field("postal_code", onchange="getAddress()", wrapper_class="col"),
                    Field("state", wrapper_class="col"),
                    Field("city", wrapper_class="col"),
                    css_class="row",
                ),
                Div(
                    Field("address", wrapper_class="col"),
                    Field("district", wrapper_class="col"),
                    css_class="row",
                ),
                Div(
                    Field("number", wrapper_class="col"),
                    Field("complement", wrapper_class="col"),
                    css_class="row",
                ),
                css_class="border-bottom mb-3",
            )
        )

class AdicionarUsuarioInstituicaoForm(forms.Form):
    """ Formulário de inclusão de usuário vinculado a uma instituição """
    cpf = forms.CharField(max_length=14)

class PesquisarPetForm(forms.Form):
    """ Formulário de pesquisa de um Pet da instituição """
    id_pet = forms.IntegerField()

class AdicionarPetInstituicao(forms.ModelForm):
    """ Formulário de inclusão de pet vinculado a uma instituição """
    class Meta:
        model = Pet
        fields = ['foto', 'nome', 'descricao', 'especie', 'raca', 'sexo', 'porte', 'dataNascimento']


class SolicitarAdocaoForm(forms.Form):
    """ Formulário de solicitação de adoção """
    nome = forms.CharField(max_length = 50)
    numero_celular = forms.CharField(max_length = 16)
    email = forms.EmailField(max_length = 150)

class DoacaoCadastroForm(forms.ModelForm):
    class Meta:
        model = INSTITUICAO
        fields = [
            'doacao_valor_20_link',
            'doacao_valor_50_link',
            'doacao_valor_100_link',
            'doacao_limpeza_link',
            'doacao_limpeza_valor',
            'doacao_alimentacao_link',
            'doacao_alimentacao_valor',
            'doacao_medicamentos_link',
            'doacao_medicamentos_valor',
            'doacao_diaria_internacao_link',
            'doacao_diaria_internacao_valor',
            'doacao_patrocinio_codigo',
            'doacao_patrocinio_valor',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "."
        self.helper.add_input(
            Submit(
                "submit",
                "Atualizar",
                css_class="btn btn-outline-dark",
            )
        )
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Field("doacao_limpeza_link", wrapper_class="col"),
                    Field("doacao_limpeza_valor", wrapper_class="col"),
                    css_class="row",
                ),
                Div(
                    Field("doacao_alimentacao_link", wrapper_class="col"),
                    Field("doacao_alimentacao_valor", wrapper_class="col"),
                    css_class="row",
                ),
                Div(
                    Field("doacao_medicamentos_link", wrapper_class="col"),
                    Field("doacao_medicamentos_valor", wrapper_class="col"),
                    css_class="row",
                ),
                Div(
                    Field("doacao_diaria_internacao_link", wrapper_class="col"),
                    Field("doacao_diaria_internacao_valor", wrapper_class="col"),
                    css_class="row",
                ),
                css_class="border-bottom mb-3",
            )
        )