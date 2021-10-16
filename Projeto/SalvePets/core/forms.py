from django import forms
from .models import Pet, USUARIO, User, ADOCAO, INSTITUICAO
from .custom_form_fields import CpfCnpjField, TelefoneField
from django.utils.translation import ugettext_lazy as _


# Criar Array de Ano de Nascimento - não sei se faz sentido mover pra arquivo separado..

BIRTH_YEAR_CHOICES  = []
for i in range(1900,2021):
    BIRTH_YEAR_CHOICES.append(str(i))

# Forms - pra mim isso aqui é o "Controller" do projeto. Masterizar isso é garantia de sucesso.

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('Nome:'))
    last_name = forms.CharField(max_length=30, label=_('Sobrenome'))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = '__all__'



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class UsuarioForm(forms.ModelForm):
    cpfCnpj = CpfCnpjField(label='CPF')
    #dataNascimento = forms.DateField(required=True, widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),input_formats=['%d/%m/%Y','%m/%d/%Y'], label=_('Data de Nascimento'))
    dataNascimento = forms.DateField(required=True, widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES), label=_('Data de Nascimento'))
    telefone = TelefoneField(required=False, label=_('Número de Telefone'))
    #receberNotificacoes = forms.BooleanField(required=False, label = 'Desejo receber notificações', help_text='(Marque este campo caso deseje ser notificado sobre pets perdidos ou encontrados.)')
    class Meta:
        model = USUARIO
        fields = ('cpfCnpj', 'dataNascimento', 'telefone', 'site', 'receberNotificacoes') #Retirei tipoUsuairo


#Classe que seria usada como "Cadastro Único" - li que é possível fazer funcionar, só preciso entender melhor como.
#Por enquanto não está implementada no Settings, então não é utilizada

class ExtendedSignupForm(SignupForm):
    cpfCnpj = forms.CharField(max_length=14, label='CPF')
    #dataNascimento = forms.DateField(required=True, widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),input_formats=['%d/%m/%Y'], label=_('Data de Nascimento'))
    dataNascimento = forms.DateField(required=True, widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES), label=_('Data de Nascimento'))
    telefone = forms.CharField(required=False, max_length=16, label=_('Número de Telefone'))
    receberNotificacoes = forms.BooleanField(required=False, label = _('Desejo receber notificações'), help_text=_('(Marque este campo caso deseje ser notificado sobre pets perdidos ou encontrados.)'))
    #siteUrl = forms.URLField(initial='http://', label='URL do seu Site')





#Projeto integrado II
class ContactForm(forms.Form):
    nome_fantasia = forms.CharField(max_length = 50)
    razao_social = forms.CharField(max_length = 50)
    numero_cnpj = forms.CharField(max_length = 18)
    numero_telefone = forms.CharField(max_length = 16)
    email_address = forms.EmailField(max_length = 150)


class AdocaoForm(forms.ModelForm):
    class Meta:
        model = ADOCAO
        fields = '__all__'

class InstituicaoForm(forms.ModelForm):
    class Meta:
        model = INSTITUICAO
        fields = ('nome_instituicao', 'razao_social', 'cnpj', 'telefone', 'email')
