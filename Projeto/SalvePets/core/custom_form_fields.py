from django import forms
from django.core import validators
from django.forms import ValidationError
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.translation import ugettext_lazy as _

class CpfCnpjField(forms.CharField):
    """ Campo de Form criado especificamente como validador do CPF:
    terá de ser alterado futuramente para validar CNPJ """
    def to_python(self, value):
        # Limpa a máscara puxando só valores numéricos
        if not value:
            return []

        value = value.replace('.','')
        value = value.replace('-','')
        return value

    def validate(self, value):
        """ Validador do CPF em si. Ele só funciona porque o Python automaticamente roda o método
        acima antes, que faz a 'limpa' """
        super().validate(value)
        tam_cpf = 11
        i=0
        j=10
        digito1 = 0
        digito2 = 0
        tam = len(value)
        if tam!=tam_cpf:
            if tam<tam_cpf:
                raise ValidationError(
                    _(f'Número de dígitos {tam} inferior ao esperado: {tam_cpf}'),
                    code='TamDivergente',
                    params={'value': '11'},
                )

            raise ValidationError(_(f'Número de dígitos {tam} superior ao esperado:{tam_cpf}'),
                                  code='TamDivergente',
                                  params={'value': '11'},
                                  )

        value_error = ['00000000000', '11111111111', '22222222222',
                        '33333333333', '44444444444', '55555555555']
        if value in value_error:
            raise ValidationError(
                _('CPF inválido. Números idênticos.'),
                code='NrosIguais',
                params={'value': '11'},
            )
        arr = list(value)
        #Validação do primeiro dígito
        for i in range(0,len(arr)-2):
            digito1 = digito1 + int(arr[i])*(j-i)
        digito1 %= 11
        if digito1 < 2:
            digito1 = 0
        else:
            digito1 = 11 - digito1
        #Validação do segundo dígito
        i=0
        j=11
        for i in range(0,len(arr)-1):
            digito2 = digito2 + int(arr[i])*(j-i)
        digito2 %= 11
        if digito2 < 2:
            digito2 = 0
        else:
            digito2 = 11 - digito2
        if not(arr[9]==str(digito1) and arr[10]==str(digito2)):
            raise ValidationError(
                _('CPF inválido.'),
                code='Invalido',
                params={'value': '01'},
            )

class TelefoneField(forms.Field):
    """ Cria uma máscara para o campo de telefone """
    def to_python(self, value):
        # Limpa a máscara puxando só valores numéricos
        if not value:
            return []

        value = value.replace('(','')
        value = value.replace(')','')
        value = value.replace('-','')
        value = value.replace(' ','')
        return value

    def validate(self, value):
        # Validador do Telefone (apenas número de Dígitos)
        super().validate(value)
        tam_telefone = 11
        tam = len(value)
        if tam>0:
            if tam!=tam_telefone:
                if tam<tam_telefone:
                    raise ValidationError(
                        f'Número de dígitos {tam} inferior ao esperado: {tam_telefone}',
                        code='TamDivergente',
                        params={'value': '11'},
                    )
                #else:
                raise ValidationError(f'Número de dígitos {tam} superior ao esperado: {tam_telefone}',
                                      code='TamDivergente',
                                      params={'value': '11'},
                                      )
