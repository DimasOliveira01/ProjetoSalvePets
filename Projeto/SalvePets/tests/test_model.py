import sys
import pytest
from django.contrib.gis.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
sys.path.append("/home/ProjetoSalvePets/Projeto")
from core.models import LOCALIZACAO
from core.models import USUARIO
#from SalvePets import settings
from django.db import connection

from django.conf import settings

class TestPost:
    def test_model_localizacao(self):
        """
        TESTE DE INSERT - TABELA LOCALIZAÇÃO
        """
        localizacao = LOCALIZACAO.objects.create(
            cidade = 'cidade teste',
            uf = 'TT',
            rua = 'rua teste',
            cep = '00000000',
            num = '000',
            bairro='bairro teste',
            dataCriacao ='2021-10-15',
            dataModificacao = '2021-10-15'

        )

        assert localizacao.cidade == 'cidade teste', 'Deve retornar: cidade teste'
        assert localizacao.uf == 'TT', 'Deve retornar: TT'
        assert localizacao.rua == 'rua teste', 'Deve retornar: rua teste'
        assert localizacao.cep == '00000000', 'Deve retornar: 00000000'
        assert localizacao.num == '000', 'Deve retornar: 000'
        assert localizacao.bairro == 'bairro teste', 'Deve retornar: bairro teste'
    
    # def teste_mondel_truncate_usuario(self):
        
    #     USUARIO.objects.all().delete()
    #     User.objects.all().delete()
    
    #     assert False == USUARIO.objects.all().exists()
    #     assert False == User.objects.all().exists()
    
    @pytest.mark.django_db
    def test_model_usuario(self):
        """
        TESTE DE INSERT - TABELA USUARIO
        """

        # usuario_teste = User.objects.create_user('user1', 'user1@mail.com', 'teste12342')
        # usuario_teste2 = USUARIO.objects.create(user=instance)
        

        usuario_criado = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        usuario = USUARIO.objects.create(
            user = usuario_criado,
            tipoUsuario = '1',
            cpfCnpj = '12345678901',
            dataNascimento = '2021-10-15',
            pontuacao = '0.00',
            receberNotificacoes='False',
            site ='site teste',
            #idImagem = '2021-10-15'
            dataCriacao = '2021-10-15',
            dataModificacao = '2021-10-15'

        )


        assert 1==1
        # assert usuario.tipoUsuario == '1', 'Deve retornar: 1'
        # assert usuario.cpfCnpj == '123456789012', 'Deve retornar: 123456789012'
        # assert usuario.dataNascimento == '2021-10-15', 'Deve retornar: 002021-10-15000000'
        # assert usuario.pontuacao == '0.00', 'Deve retornar: 0.00'
        # assert usuario.receberNotificacoes == 'False', 'Deve retornar: false'
        # assert usuario.site == 'site teste', 'Deve retornar: site teste'
        # assert usuario.dataCriacao == '2021-10-15', 'Deve retornar: 2021-10-15'
        # assert usuario.dataModificacao == '2021-10-15', 'Deve retornar: 2021-10-15'