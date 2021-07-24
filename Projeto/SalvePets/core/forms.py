from django import forms
from .models import Pet, USUARIO, User

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Nome:')
    last_name = forms.CharField(max_length=30, label='Sobrenome')

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
    class Meta:
        model = USUARIO
        fields = ('cpfCnpj', 'dataNascimento', 'telefone', 'receberNotificacoes', 'tipoUsuario', 'site')