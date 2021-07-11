from django import forms
from .models import Pet

# Arquivo para criação dos nossos FORMS caso prefiram.

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = '__all__'


class MeuCadastroForm(forms.Form):
	first_name = forms.CharField(max_length = 50)
	last_name = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)
	#message = forms.CharField(widget = forms.Textarea, max_length = 2000)
