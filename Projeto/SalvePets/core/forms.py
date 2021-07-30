from django import forms
from .models import Pet, USUARIO, User
from django.utils.translation import ugettext_lazy as _

BIRTH_YEAR_CHOICES  = []
for i in range(1900,2021):
    BIRTH_YEAR_CHOICES.append(str(i))

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
    #cpfCnpj = forms.CharField(max_length=14, label='CPF')
    #dataNascimento = forms.DateField(required=True, widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),input_formats=['%d/%m/%Y'], label='Data de Nascimento')
    #telefone = forms.CharField(required=False, max_length=16, label='Nro de Telefone')
    #receberNotificacoes = forms.BooleanField(required=False, label = 'Desejo receber notificações', help_text='(Marque este campo caso deseje ser notificado sobre pets perdidos ou encontrados.)')
    class Meta:
        model = USUARIO
        fields = ('cpfCnpj', 'dataNascimento', 'telefone', 'receberNotificacoes') #Retirei tipoUsuairo e site


#Classe que seria usada como "Cadastro Único" - li que é possível fazer funcionar, só preciso entender melhor como.
#Por enquanto não está implementada no Settings, então não é utilizada

class ExtendedSignupForm(SignupForm):
    cpfCnpj = forms.CharField(max_length=14, label='CPF')
    dataNascimento = forms.DateField(required=True, widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),input_formats=['%d/%m/%Y'], label='Data de Nascimento')
    telefone = forms.CharField(required=False, max_length=16, label='Nro de Telefone')
    receberNotificacoes = forms.BooleanField(required=False, label = 'Desejo receber notificações', help_text='(Marque este campo caso deseje ser notificado sobre pets perdidos ou encontrados.)')
    #siteUrl = forms.URLField(initial='http://', label='URL do seu Site')