import os
from collections import namedtuple
from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect
from django.db import connection
from django.core import mail
from django.utils.html import strip_tags
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django.core.mail import message, send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from geopy.geocoders import Nominatim
from django.db.models import Sum
from django.db.models import Count

from .forms import ContactForm
from .forms import UserForm, UsuarioForm, InstituicaoForm, AdicionarUsuarioInstituicaoForm, AdicionarPetInstituicao, SolicitarAdocaoForm, PesquisarPetForm, DoacaoCadastroForm
from .models import AVALIACAO, PATROCINIO, Pet, USUARIO, INSTITUICAO

# === Funções com render simples ===

def index(request):
    """ Tela inicial """
    #user_form = UserForm(instance=request.user)
    #usuario_form = UsuarioForm(instance=request.user.usuario)
    #cadastro_incompleto = False
    #if usuario_form.cpfcnpj == "":
    #    cadastro_incompleto = True
    #    return render(request, 'index.html', {'cadastro_incompleto', cadastro_incompleto})
    #else:
    #    return render(request, 'index.html',{'cadastro_incompleto', cadastro_incompleto})
    return render(request, 'index.html')


def sobre(request):
    """ Tela 'sobre' """
    return render(request, 'sobre.html')


def em_construcao(request):
    """ Tela que exibe a mensagem 'em construção' """
    return render(request, 'emconstrucao.html')

def faq(request):
    """ Tela de faq """
    return render(request, 'faq.html')



# ==================================

# ===      Funções gerais        ===

def lista_pets_encontrados(request):
    """ Tela de lista de pets encontrados """
    pet=Pet.objects.filter(encontradoPerdido='Encontrado', ativo=True)
    #& Pet.objects.filter(ativo=True) # & encontradoPerdido='encontrado' ativo=True
    return render(request, 'listaPetsEncontrados.html',{'pet':pet})


def lista_pets_perdidos(request):
    """ Tela de lista de pets perdidos """
    pet=Pet.objects.filter(encontradoPerdido='Perdido', ativo=True)
    return render(request, 'listaPetsPerdidos.html',{'pet':pet})


@login_required(login_url='/accounts/login')
def lista_pets_usuario(request):
    """ Tela de lista de pets de um usuário """
    pet=Pet.objects.filter(ativo=True, user=request.user,fk_id_instituicao=None)
    return render(request, 'listaPetsUsuario.html',{'pet':pet})


@login_required(login_url='/accounts/login')
def cadastro_pet(request):
    """ Tela de cadastro de pet """
    pet_id=request.GET.get('id')
    if pet_id:
        pet=Pet.objects.get(id=pet_id)
        if pet.user == request.user:
            return render(request,'cadastroPet.html',{'pet':pet})
    return render (request, 'cadastroPet.html')


@login_required(login_url='/accounts/login')
def set_pet(request):
    """ Cadastro e atualização de um pet """
    nome=request.POST.get('nome')
    descricao=request.POST.get('descricao')
    dataPerdaEncontro=request.POST.get('dataPerdaEncontro')
    especie=request.POST.get('especie')
    raca=request.POST.get('raca')
    sexo=request.POST.get('sexo')
    cor=request.POST.get('cor')
    porte=request.POST.get('porte')
    peso=request.POST.get('peso')
    encontradoPerdido=request.POST.get('encontradoPerdido')
    coordenada=request.POST.get('coordenada')
    foto=request.FILES.get('foto')
    user=request.user

    # Atualização de cadastro de um pet
    pet_id=request.POST.get('pet-id')

    if pet_id:
        pet=Pet.objects.get(id=pet_id)

        # Tamanho máximo de arquivo
        if foto:
            MAX_SIZE = 2097152
            file = request.FILES['foto']
            extensao = os.path.splitext(file.name)[1]
            extensao_valida = ['.png', '.jpg', '.jpeg', '.bmp']

            if not extensao in extensao_valida:
                return redirect(f'/cadastro-pet/?id={pet.id}')

            if file.size > MAX_SIZE:
                return redirect(f'/cadastro-pet/?id={pet.id}')

        if user == pet.user:
            if nome:
                pet.nome=nome
                pet.save()
            else:
                pet.nome="Sem nome"
                pet.save()

            if descricao:
                pet.descricao=descricao
                pet.save()

            if dataPerdaEncontro:
                pet.dataPerdaEncontro=dataPerdaEncontro
                pet.save()

            if especie:
                pet.especie=especie
                pet.save()

            if raca:
                pet.raca=raca
                pet.save()

            if sexo:
                pet.sexo=sexo
                pet.save()

            if cor:
                pet.cor=cor
                pet.save()

            if porte:
                pet.porte=porte
                pet.save()

            if peso:
                pet.peso=peso
                pet.save()

            if encontradoPerdido:
                pet.encontradoPerdido=encontradoPerdido
                pet.save()

            if coordenada:
                pet.coordenada=coordenada
                pet.save()

            if foto:
                pet.foto = foto
                pet.save()
    #Cadastro de um novo Pet
    else:
        if foto:
            max_size = 2097152
            file = request.FILES['foto']
            extensao = os.path.splitext(file.name)[1]
            print(extensao)
            extensao_valida = ['.png', '.jpg', '.jpeg', '.bmp']

            if not extensao in extensao_valida:
                erro = "Os formatos de imagem permitidos são PNG, JPG, JPEG e BMP."
                return render(request, 'cadastroPet.html', {'erro': erro})

            if file.size > max_size:
                erro = "O tamanho da imagem deve ser menor que 2 MB"
                return render(request, 'cadastroPet.html', {'erro': erro})

        pet = Pet.objects.create(porte=porte, encontradoPerdido=encontradoPerdido, foto=foto,
                                 user=user, coordenada=coordenada, sexo=sexo)
        if nome:
            pet.nome=nome
        else:
            pet.nome="Sem nome"
            pet.save()
        if descricao:
            pet.descricao = descricao
            pet.save()
        if dataPerdaEncontro:
            pet.dataPerdaEncontro = dataPerdaEncontro
            pet.save()
        if especie:
            pet.especie = especie
            pet.save()
        if raca:
            pet.raca = raca
            pet.save()
        if cor:
            pet.cor = cor
            pet.save()
        if peso:
            pet.peso = peso
            pet.save()

        # Gatilho da notificação de pet encontrado/perdido
        notif_pet_encontrado(pet.id)

    url = f'/pet-informacao/{pet.id}/'
    return redirect(url)


@login_required(login_url='/acccounts/login')
def deletar_pet(request, id):
    """ Tela de exclusão de pet """
    pet=Pet.objects.get(id=id)
    if pet.user == request.user:
        pet.delete()
    return redirect('/lista-pet-usuario')


#@login_required(login_url='/accounts/login')
def pet_informacao(request, id):
    """ Tela de informação de pet """
    pet = Pet.objects.get(ativo=True, id=id)
    creator = pet.user

    try:
        #Localização reversa
        geolocator = Nominatim(user_agent="salve-pets")
        coordenadas = str(pet.coordenada[1]) + ',' + str(pet.coordenada[0])

        location_request = geolocator.reverse(coordenadas)
        raw_location = location_request.raw['address']

        strings = [
            raw_location.get('road'),
            raw_location.get('house_number'),
            raw_location.get('postcode'),
            raw_location.get('suburb'),
            raw_location.get('state'),
            raw_location.get('country')
        ]

        location = ', '.join(filter(None, strings))
    except Exception:
        location = "Erro na obtenção da localização do pet"

    return render(request, 'pet.html', {'pet':pet,'creator':creator, 'localizacao': location})

@login_required
@transaction.atomic
def modificar_cadastro(request):
    """ Tela para alterar cadastro de usuário """
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        usuario_form = UsuarioForm(request.POST, instance=request.user.usuario)
        if usuario_form.is_valid() and user_form.is_valid():
            user_form.save()
            usuario_form.save()
            return render(request, 'index.html')
        #else:
        messages.error(request, ('Please correct the error below.'))
    else:
        usuario_form = UsuarioForm(instance=request.user.usuario)
        user_form = UserForm(instance=request.user)
    return render(request, 'modificar-cadastro.html', {
        'usuario_form': usuario_form,
        'user_form': user_form,
    })

@login_required
@transaction.atomic
def completar_cadastro(request):
    """ Tela para completar cadastro de usuário """
    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST, instance=request.user.usuario)
        if usuario_form.is_valid():
            usuario_form.save()
            return render(request, 'index.html')
        #else:
        messages.error(request, ('Please correct the error below.'))
    else:
        usuario_form = UsuarioForm(instance=request.user.usuario)
    return render(request, 'completar-cadastro.html', {
        'usuario_form': usuario_form,
    })


"""
def sobre(request):
    return render(request, 'sobre.html')
def em_construcao(request):
    return render(request, 'emconstrucao.html')
"""

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def notif_pet_encontrado(id):
    """ Conexão com o banco de dados sobre notificação de pet encontrado """
    try:
        # Conexão com o banco
        cursor = connection.cursor()

        # Retorna dados do pet que está sendo cadastrado agora
        pet_query = '''SELECT pet.id, pet.coordenada, pet."encontradoPerdido", usr.email, pet.foto,
                        pet.nome, pet."dataPerdaEncontro", pet.especie, pet.porte
                        FROM core_pet AS pet
                        INNER JOIN auth_user AS usr on usr.id = pet.user_id
                        WHERE pet.id = %s'''
        cursor.execute(pet_query,[id])
        pet = namedtuplefetchall(cursor)
        
        ''' Garante que a pessoa que cadastrou um pet perdido vai receber e-mails apenas de pets
        encontrados próximos a região, e vice-versa. '''
        if pet[0].encontradoPerdido == "perdido":
            encontrado_perdido_pesquisar = "encontrado"
        else:
            encontrado_perdido_pesquisar = "perdido"

        if pet[0].dataPerdaEncontro:
            perdido_inicio = pet[0].dataPerdaEncontro - timedelta(days = 60)
            perdido_fim = pet[0].dataPerdaEncontro + timedelta(days = 60)
        else:
            perdido_inicio = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
            perdido_fim = datetime.strptime('2100-01-01', '%Y-%m-%d').date()

        # Query para pegar os campos para o envio do e-mail e cálculo da distância
        query = '''SELECT pet.id, pet.nome, usr.email, pet.foto, usuario."receberNotificacoes",
                        pet.coordenada
                        FROM core_pet AS pet
                        INNER JOIN core_usuario AS usuario ON usuario.user_id = pet.user_id
                        INNER JOIN auth_user AS usr ON usr.id = usuario.user_id
                        WHERE pet."encontradoPerdido" = %s AND pet."dataPerdaEncontro" BETWEEN %s AND %s
                            AND pet.especie = %s AND pet.porte BETWEEN %s and %s
                        ORDER BY pet.id
                        '''

        # Execução da query e inserção dos dados em uma Named Tuple
        cursor.execute(query,[encontrado_perdido_pesquisar, perdido_inicio, perdido_fim,
                              pet[0].especie, pet[0].porte - 30, pet[0].porte + 30 ])
        pets = namedtuplefetchall(cursor)

        # Caso existam pets no banco de dados
        if pets:
            distancias = []
            id_list = []
            nome_list = []
            foto_list = []
            count = 0

            # Calcula distância desse pet cadastrado com todos os outros no banco de dados
            for i in range(len(pets)):
                if pet[0].id != pets[i].id:
                    cursor.execute("SELECT ST_DistanceSphere('" + pet[0].coordenada +
                                   "','" + pets[i].coordenada + "')::numeric::integer")
                    distancias.append(cursor.fetchone())

            # Se o cálculo retornou algo
            if distancias:
                for list in distancias:
                    for valor in list:
                        # Percorre por todas as distâncias para caso seja menor que 10km,
                        # inicia o processo de envio de e-mail               
                        if valor <= 10000 and pets[count].receberNotificacoes is True:
                            if pet[0].encontradoPerdido == "encontrado":
                                # Passa as informações do dono do pet próximo para o envio do e-mail
                                if pet[0].email != pets[count].email:
                                    enviar_email_pet_encontrado(pet[0].id, str(pets[count].email),
                                                                pet[0].foto, pet[0].nome)
                            else:
                                ''' Armazena em lista todos os nomes e fotos dos pets para enviar
                                por e-mail a quem está cadastrando. '''
                                if pet[0].email != pets[count].email:
                                    id_list.append(pets[count].id)
                                    nome_list.append(pets[count].nome)
                                    foto_list.append(pets[count].foto)
                        count = count + 1

                if id_list and foto_list and nome_list:
                    # Envia lista de pets encontrados para quem cadastrou um pet perdido.
                    enviar_email_pet_perdido(id_list, str(pet[0].email), foto_list, nome_list)
    except Exception as error:
        print("Falha em ler o banco de dados.\n", error)
    finally:
        if connection:
            connection.close()


def enviar_email_pet_encontrado(id, email, foto, nome_pet):
    """ Tela de envio de notificação de pet encontrado """
    id = str(id)
    assunto = _("Encontramos um pet semelhante ao seu")
    remetente = os.environ.get("EMAIL_HOST_USER")
    destinatario = str(email)
    nome_pet = str(nome_pet)

    html = loader.render_to_string('emails/pet_encontrado.html',
                                   {'id': id, 'foto': foto, 'nome_pet': nome_pet})
    plain_message = strip_tags(html)

    # Envio do e-mail
    mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)

def enviar_email_pet_perdido(id, email, foto, nome_pet):
    """ Tela de envio de notificação de pet perdido """
    assunto = _("Novos pets parecidos com o seu foram encontrados")
    remetente = os.environ.get("EMAIL_HOST_USER")
    destinatario = str(email)

    html = loader.render_to_string('emails/pet_perdido.html',
                                   {'id': id, 'foto': foto, 'nome_pet': nome_pet})
    plain_message = strip_tags(html)

    # Envio do e-mail
    mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)

# ==================================
#Funções Projeto Integrado II

#Formulário para solicitar cadastro de Instituição

def cadastro_empresa(request):
    """ Tela de cadastro de instituição """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Solicitação de cadastro de empresa"
            body = {
                'nome_fantasia': form.cleaned_data['nome_fantasia'],
                'razao_social': form.cleaned_data['razao_social'],
                'numero_cnpj': form.cleaned_data['numero_cnpj'],
                'numero_telefone': form.cleaned_data['numero_telefone'],
                'email_address': form.cleaned_data['email_address'],
            }
            message = "\n".join(body.values())

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      ['atendimentoSalvePets@gmail.com'],
        fail_silently=False) 
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return render(request, "index.html")
        #return redirect ("sobre.html")
            
    form = ContactForm()
    return render(request, "instituicao/formInstituicao.html", {'form':form})




@login_required
@transaction.atomic
def completar_cadastro_instituicao(request):
    """ Tela para completar o cadastro de uma instituição """
    if request.method == "POST":
        if request.user.usuario.fk_instituicao:

            instance=request.user.usuario.fk_instituicao
            product = INSTITUICAO.objects.get(id=instance.id)

            form = InstituicaoForm(request.POST, instance=product)
            if form.is_valid():
                form.save()

                usuario=request.user.usuario
                user=request.user
                instituicao=INSTITUICAO.objects.get(id=instance.id)
                email = os.environ.get("EMAIL_HOST_USER")
                assunto = _("Solicitação de cadastro de Instituição!")
                remetente = os.environ.get("EMAIL_HOST_USER")
                destinatario = str(email)
                html = loader.render_to_string('instituicao/email/email-solicitacao-cadastro-instituicao.html',
                                               {'instituicao': instituicao, 'usuario':usuario, 'user': user})
                plain_message = strip_tags(html)

                # Envio do e-mail
                mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)

                return render(request, 'instituicao/administrativoInstituicao.html')
            #else:
            messages.error(request, ('Por favor corriga o erro abaixo!'))
        else:
            form = InstituicaoForm(request.POST)
            if form.is_valid():
                instancia = form.save()
                usuario = request.user.usuario
                USUARIO.objects.filter(id=usuario.id).update(fk_instituicao_id=instancia.id)

                instituicao=INSTITUICAO.objects.get(id=instancia.id)
                email = os.environ.get("EMAIL_HOST_USER")
                assunto = _("Solicitação de cadastro de Instituição!")
                remetente = os.environ.get("EMAIL_HOST_USER")
                destinatario = str(email)            
                html = loader.render_to_string('instituicao/email/email-solicitacao-cadastro-instituicao.html',
                                               {'instituicao': instituicao})
                plain_message = strip_tags(html)

                # Envio do e-mail
                mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)


                return render(request, 'instituicao/administrativoInstituicao.html')
            #else:
            messages.error(request, ('Por favor corriga o erro abaixo!'))
    else:
        form = InstituicaoForm(instance=request.user.usuario.fk_instituicao)
    id_user=request.user.id
    usuario=USUARIO.objects.get(id=id_user)
    return render(request, 'instituicao/modificar-cadastro-instituicao.html', {
        'form': form, 'usuario':usuario
    })

''' print('cpf enviado no post = ', cpf)
    id_instituicao = USUARIO.objects.filter(id=usuario.id)
    print ('id da instituicao do usuario = ', id_instituicao[0].fk_instituicao_id)
    res_filtro = USUARIO.objects.filter(cpfcnpj=cpf)
    print('id do usuário que possui o mesmo cpf do post: ', res_filtro[0].id)
    len(res_filtro)
    print('tamanhao do vetor: ', len(res_filtro))
    #USUARIO.objects.filter(request.POST.get('cpf')==teste)
    INSTITUICAO.objects.get(id=usuario[i].fk_instituicao_id)
'''

'''
pet=Pet.objects.filter(encontradoPerdido='Encontrado', ativo=True)
instituicao=INSTITUICAO.objects.filter(encontradoPerdido='Encontrado', ativo=True)
'''

def teste(request):
    """ tela de teste """
    return render(request, 'teste.html')

def adotar(request):
    """ Exibe a tela de cadastro de adoção """
    return render(request, 'adotar/cadastro_adotar.html')

@login_required
@transaction.atomic
def adicionar_usuario_instituicao(request):
    """ Adiciona um usuário em uma determinada instituição """
    if request.user.usuario.is_admin_instituicao is True:
        form = AdicionarUsuarioInstituicaoForm()
        if request.method == "POST":
            #obtêm o dado do usuário logado
            usuario = request.user.usuario
            #obtêm o dado enviado no POST
            cpf=request.POST.get('cpf')
            #Obtêm o objeto usuario que tem o mesmo cpf do POST
            res_filtro = USUARIO.objects.filter(cpfcnpj=cpf)

            #print(user[0].email)
            if len(res_filtro)>0:
                user=User.objects.filter(id=res_filtro[0].user_id)
                id_instituicao = USUARIO.objects.filter(id=usuario.id)
                USUARIO.objects.filter(cpfcnpj=cpf).update(fk_instituicao_id=id_instituicao[0].fk_instituicao_id)
                #form = AdicionarUsuarioInstituicaoForm(request.POST)
                #print (request.POST.get('cpf'))
                
                instituicao=INSTITUICAO.objects.filter(id=id_instituicao[0].fk_instituicao_id)
                email = user[0].email
                msgm=("Solicitação de cadastro na Instituição: " + str(instituicao[0].nome_instituicao))
                assunto = _(msgm)
                remetente = os.environ.get("EMAIL_HOST_USER")
                destinatario = str(email)
                html = loader.render_to_string('instituicao/email/email-cadastro-usuario-instituicao.html',
                                               {'user': user[0].first_name,
                                                'instituicao': instituicao[0].nome_instituicao})
                plain_message = strip_tags(html)

                # Envio do e-mail
                mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)

                

                return render(request, 'instituicao/mensagem/confirmacao-cadastro.html')
            #else:
            messages.error(request, 'Por favor selecione um usuário existente!')
        id_user=request.user.id
        usuario=USUARIO.objects.get(id=id_user)
        return render(request, 'instituicao/adicionar-usuario-instituicao.html', {
            'form': form, 'usuario': usuario
        })
    #else:
    user=request.user.usuario
    return render(request, 'instituicao/acesso-proibido.html',{'user':user})

@login_required
@transaction.atomic
def listar_usuario_instituicao(request):
    """ Lista os usuários de uma determinada instituição """
    if request.user.usuario.is_admin_instituicao is True:
        cursor = connection.cursor()
        id_inst=request.user.usuario.fk_instituicao_id
        #usuario=USUARIO.objects.filter(User__type=User.is_active) #tipoUsuario='Usuário comum'
        #user=User.objects.filter(tipoUsuario='Usuário comum')
        query = ''' select tab1.first_name as nome1, tab1.last_name as nome2, tab2.cpfcnpj as cpf,
                    tab2.id, tab2.fk_instituicao_id from auth_user as tab1 
                    inner join core_usuario as tab2 on (tab1.id=tab2.user_id) 
                    where tab2.fk_instituicao_id is Not NULL and tab2.fk_instituicao_id = %s'''
        cursor.execute(query, [id_inst])
        usuario = namedtuplefetchall(cursor)
        if len(usuario)==0:
            messages.error(request, 'Nenhum usuário existente!')
        id_user=request.user.id
        usuario1=USUARIO.objects.get(id=id_user)
        return render(request,
                      'instituicao/listar-usuario-instituicao.html',{'usuario':usuario,
                                                                     'usuario1': usuario1})
    #else:
    return render(request, 'instituicao/acesso-proibido.html')

@login_required(login_url='/acccounts/login')
@transaction.atomic
def deletar_usuario_instituicao(request, id):
    """ Exclui um usuário de uma determinada instituição """
    USUARIO.objects.filter(id=id).update(fk_instituicao_id=None)
    return redirect('/listar-usuario-instituicao/')

@login_required(login_url='/accounts/login')
def cadastro_pet_instituicao(request):
    """ Cadastro de um pet de uma determinada instituição """
    cursor = connection.cursor()
    id_inst=request.user.usuario.fk_instituicao_id
    query = '''select * from core_usuario where fk_instituicao_id=%s and is_admin_instituicao=True'''
    cursor.execute(query, [id_inst])
    usuario = namedtuplefetchall(cursor)
    if len(usuario)>0:
        existe_admin=1
    else:
        existe_admin=0
    
    id_user=request.user.id
    usuario=USUARIO.objects.get(id=id_user)
    if(request.user.usuario.fk_instituicao_id is not None and existe_admin==1):
        pet_id=request.GET.get('id')
        if pet_id:
            pet=Pet.objects.get(id=pet_id)
            #if pet.user == request.user:
            return render(request,'instituicao/cadastro-pet-instituicao.html',{'pet':pet,'usuario': usuario})
        return render (request, 'instituicao/cadastro-pet-instituicao.html',{'usuario': usuario})
    #else:
    return render(request, 'instituicao/acesso-proibido.html')

@login_required(login_url='/acccounts/login')
def set_pet_instituicao(request):
    """ Cadastro e atualização de um pet de uma determinada instituição """
    nome=request.POST.get('nome')
    ativo=request.POST.get('ativo')
    adotado=request.POST.get('adotado')
    descricao=request.POST.get('descricao')
    especie=request.POST.get('especie')
    raca=request.POST.get('raca')
    sexo=request.POST.get('sexo')
    porte=request.POST.get('porte')
    foto=request.FILES.get('foto')
    user=request.user
    fk_id_instituicao_id=request.user.usuario.fk_instituicao_id
    pet_id=request.POST.get('pet-id')
    
    email=request.POST.get('email')

    # Atualização de cadastro
    
    if pet_id:
    
        pet=Pet.objects.get(id=pet_id)
        if pet.fk_id_instituicao_id == request.user.usuario.fk_instituicao_id:
            if nome:
                pet.nome=nome
                pet.save()
            else:
                pet.nome="Sem nome"
                pet.save()

            if ativo=='on':
                pet.ativo=True
                pet.save()
            else:
                pet.ativo=False 
                pet.save()

            if adotado=='on':
                pet.adotado=True
                pet.save()
            else:
                pet.adotado=False 
                pet.save()

            if descricao:
                pet.descricao=descricao
                pet.save()
            
            if especie:
                pet.especie=especie
                pet.save()

            if raca:
                pet.raca=raca
                pet.save()
            
            if sexo:
                pet.sexo=sexo
                pet.save()

            if porte:
                pet.porte=porte
                pet.save()

            if foto:
                pet.foto = foto
                pet.save()
    #cadastro de um novo pet na Instituição
    else:
        if ativo=='on':
            ativo=True
        else:
            ativo=False

        if adotado=='on':
            adotado=True
        else:
            adotado=False

        pet = Pet.objects.create(adotado=adotado, ativo=ativo, porte=porte, foto=foto, user=user, sexo=sexo,
                                 fk_id_instituicao_id=fk_id_instituicao_id)
        if nome:
            pet.nome=nome
        else:
            pet.nome="Sem nome"
            pet.save()

        if ativo:
            pet.ativo=ativo
            pet.save()
        
        if adotado:
            pet.adotado=adotado
            pet.save()

        if descricao:
            pet.descricao = descricao
            pet.save()
        if especie:
            pet.especie = especie
            pet.save()
        if raca:
            pet.raca = raca
            pet.save()

    if email:
        us=User.objects.filter(email=email)
        if us:
            pet.fk_id_usuario_adocao_id=us[0].id
            pet.save()
            
            #envio de email de avaliação da instituição
            assunto =_("Opine sobre a adoção do seu Pet")
            remetente = os.environ.get("EMAIL_HOST_USER")
            destinatario=(email)
            html = loader.render_to_string('instituicao/email/email-avaliacao-instituicao.html',{'us': us[0], 'pet': pet})
            plain_message = strip_tags(html)
            # Envio do e-mail
            mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)



    else:
        pet.fk_id_usuario_adocao_id=None
        pet.save() 

    url = f'/pet-informacao-instituicao/{pet.id}/'
    return redirect (url)

#avaliacao_instituicao
@login_required(login_url='/accounts/login')
def avaliacao_instituicao(request):
    return render(request, 'instituicao/avaliacao-instituicao.html')

"""
    user = request.user
    usuario = request.user.usuario
    pet = Pet.objects.get(id=id)
    instituicao=INSTITUICAO.objects.filter(id=pet.fk_id_instituicao_id)
    email = instituicao[0].email
    assunto = _("Solicitação de adoção de Pet")
    remetente = os.environ.get("EMAIL_HOST_USER")
    destinatario = str(email)
    html = loader.render_to_string('instituicao/email/email-solicitar-adocao.html',
                                   {'user': user, 'usuario': usuario, 'pet': pet})
    plain_message = strip_tags(html)

    # Envio do e-mail
    mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)
"""



@login_required(login_url='/accounts/login')
def pet_informacao_instituicao(request, id):
    """ Tela de informações sobre uma determinada instituição """
    pet = Pet.objects.get(id=id)
    inst=INSTITUICAO.objects.get(id=pet.fk_id_instituicao_id)
    id_user=request.user.id
    usuario=USUARIO.objects.get(id=id_user)
    print(id_user,'adfagadgfa')
    print(inst.nome_instituicao)
    return render(request, 'instituicao/pet-instituicao.html',
                  {'pet':pet,'inst':inst,'usuario':usuario})


def pet_informacao_instituicao_adocao(request, id):
    """ Tela de informações sobre regras de adoção de uma determinada instituição """
    pet = Pet.objects.get(id=id)
    inst=INSTITUICAO.objects.get(id=pet.fk_id_instituicao_id)
    #determinando a nota média dos usuários
    media=0
    count=0
    soma=0
    #itens = AVALIACAO.objects.all()
    itens = AVALIACAO.objects.filter(fk_id_instituicao_id=pet.fk_id_instituicao_id)
    soma = sum(itens.values_list('nota', flat=True))
    count=len(itens)
    if count<1:
        media=0
    else:
        media=int(soma/count)
    return render(request, 'instituicao/pet-instituicao-adocao.html', {'pet':pet,'inst':inst,'media':media,'itens':itens,'count':count})

def lista_pets_instituicao(request):
    """ Lista de pets de uma determinada instituição a serem adotados """
    cursor = connection.cursor()
    id_inst=request.user.usuario.fk_instituicao_id
    query = '''select * from core_usuario where fk_instituicao_id=%s and is_admin_instituicao=True'''
    cursor.execute(query, [id_inst])
    usuario = namedtuplefetchall(cursor)
    if len(usuario)>0:
        existe_admin=1
    else:
        existe_admin=0

    id_user=request.user.id
    usuario=USUARIO.objects.get(id=id_user)
    if(request.user.usuario.fk_instituicao_id is not None  and existe_admin==1):
        id_instituicao_usuario=request.user.usuario.fk_instituicao_id
        pet=Pet.objects.filter(encontradoPerdido=None, fk_id_instituicao_id=id_instituicao_usuario)
        id_user=request.user.id
        usuario=USUARIO.objects.get(id=id_user)
        form = PesquisarPetForm()
        if request.method == "POST":
            #obtêm o dado enviado no POST
            id_pet=request.POST.get('id_pet')
            pet = Pet.objects.filter(id=id_pet, fk_id_instituicao_id=id_instituicao_usuario)
            verifica_pesquisa=True
            return render(request, 'instituicao/lista-pets-instituicao.html',{'verifica_pesquisa':verifica_pesquisa, 'form': form, 'pet':pet,
                                                                          'usuario': usuario})
        else:
            verifica_pesquisa=False
            return render(request, 'instituicao/lista-pets-instituicao.html',{'verifica_pesquisa':verifica_pesquisa,'form': form, 'pet':pet,
                                                                          'usuario': usuario})
    #else:
    return render(request, 'instituicao/acesso-proibido-lista-pet.html')



"""
def adicionar_usuario_instituicao(request):
    if request.user.usuario.is_admin_instituicao is True:
        form = AdicionarUsuarioInstituicaoForm()
        if request.method == "POST":
            #obtêm o dado do usuário logado
            usuario = request.user.usuario
            #obtêm o dado enviado no POST
            cpf=request.POST.get('cpf')
            #Obtêm o objeto usuario que tem o mesmo cpf do POST
            res_filtro = USUARIO.objects.filter(cpfcnpj=cpf)

            #print(user[0].email)
            if len(res_filtro)>0:
                user=User.objects.filter(id=res_filtro[0].user_id)
                id_instituicao = USUARIO.objects.filter(id=usuario.id)
                USUARIO.objects.filter(cpfcnpj=cpf).update(fk_instituicao_id=id_instituicao[0].fk_instituicao_id)
                #form = AdicionarUsuarioInstituicaoForm(request.POST)
                #print (request.POST.get('cpf'))
                
                return render(request, 'instituicao/mensagem/confirmacao-cadastro.html')
            #else:
            messages.error(request, 'Por favor selecione um usuário existente!')
        id_user=request.user.id
        usuario=USUARIO.objects.get(id=id_user)
        return render(request, 'instituicao/adicionar-usuario-instituicao.html', {
            'form': form, 'usuario': usuario
        })
    #else:
    user=request.user.usuario
    return render(request, 'instituicao/acesso-proibido.html',{'user':user})
"""





def lista_pets_adocao(request):
    """ Tela que exibe a lista de pets a serem adotados """
    pet=Pet.objects.filter(encontradoPerdido=None, ativo=True, adotado=False)
    return render(request, 'instituicao/lista-pet-adocao.html',{'pet':pet})

@login_required(login_url='/accounts/login')
def meus_pets_adotados(request):
    """Tela que exibe os pets adotados por um usuário"""
    id_usuario=request.user.usuario.id
    pet=Pet.objects.filter(encontradoPerdido=None, adotado=True,fk_id_usuario_adocao_id=id_usuario)
    return render(request, 'instituicao/meus-pets-adotados.html', {'pet':pet})

@login_required(login_url='/accounts/login')
def lista_pets_usuario_instituicao(request):
    """ conferir esta função, mas acho que precisa retirar """
    pet=Pet.objects.filter(ativo=True, user=request.user)
    return render(request, 'listaPetsUsuario.html',{'pet':pet})

@login_required(login_url='/acccounts/login')
def deletar_pet_instituicao(request, id):
    """" Tela para excluir um pet de uma instituição"""
    pet=Pet.objects.get(id=id)
    if pet.fk_id_instituicao_id == request.user.usuario.fk_instituicao_id:
        pet.delete()
    return redirect('/lista-pet-instituicao/')

@login_required(login_url='/acccounts/login')
def administrativo_instituicao(request):
    """ Tela para administrar a instituição """
    id_user=request.user.id
    usuario=USUARIO.objects.get(id=id_user)
    return render(request, 'instituicao/administrativoInstituicao.html',{'usuario':usuario})
'''
@login_required
def solicitar_adocao(request):
    user = request.user
    form_usuario = UserForm()
    if request.method == 'POST':
        form = SolicitarAdocaoForm(request.POST)
        if form.is_valid():
            subject = "Solicitação de adoção de Pet"
            body = {'nome': form.cleaned_data['nome'], 'numero_celular':
            form.cleaned_data['numero_celular'], 'email': form.cleaned_data['email'],}
            message = '\n'.join(body.values())
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER,
                ['COLOCAR EMAIL DA INSTITUICAO'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return render(request, "index.html")
    form = SolicitarAdocaoForm()
    return render(request, 'instituicao/solicitar-adocao.html', {'form':form})
'''
@login_required
def solicitar_adocao(request, id):
    """ Função que apresenta a tela de pedido de adoção """
    user = request.user
    usuario = request.user.usuario
    pet = Pet.objects.get(id=id)
    instituicao=INSTITUICAO.objects.filter(id=pet.fk_id_instituicao_id)
    email = instituicao[0].email
    assunto = _("Solicitação de adoção de Pet")
    remetente = os.environ.get("EMAIL_HOST_USER")
    destinatario = str(email)
    html = loader.render_to_string('instituicao/email/email-solicitar-adocao.html',
                                   {'user': user, 'usuario': usuario, 'pet': pet})
    plain_message = strip_tags(html)

    # Envio do e-mail
    mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)

    '''
    user = request.user
    pet=Pet.objects.get(id=id)
    instituicao= INSTITUICAO.objects.filter(id=pet.fk_id_instituicao_id)
    subject = "Solicitação de adoção de Pet"
    body = {'Código do Pet': id, 'nome': user.first_name, 'numero_celular':
    user.usuario.telefone, 'email': user.email}
    message = '\n'.join(body.values())
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instituicao[0].email],
        fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found')
    '''
    return render(request, "instituicao/mensagem/solicitar-adocao.html")

'''def deletar_pet(request, id):
    pet=Pet.objects.get(id=id)
    if pet.user == request.user:
        pet.delete()
    return redirect('/lista-pet-usuario')'''

'''@transaction.atomic
def modificar_cadastro(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        usuario_form = UsuarioForm(request.POST, instance=request.user.usuario)
        if usuario_form.is_valid() and user_form.is_valid():
            user_form.save()
            usuario_form.save()   
            return render(request, 'index.html')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
            usuario_form = UsuarioForm(instance=request.user.usuario)
            user_form = UserForm(instance=request.user)
    return render(request, 'modificar-cadastro.html', {
        'usuario_form': usuario_form,
        'user_form': user_form,
    })'''

"""@login_required
@transaction.atomic
def adicionar_usuario_instituicao(request):
    if (request.user.usuario.fk_instituicao_id != None):
        form = AdicionarUsuarioInstituicaoForm()
        if request.method == "POST":
            #obtêm o dado do usuário logado
            usuario = request.user.usuario
            #obtêm o dado enviado no POST
            cpf=request.POST.get('cpf')
            #Obtêm o objeto usuario que tem o mesmo cpf do POST
            res_filtro = USUARIO.objects.filter(cpfcnpj=cpf)
            if len(res_filtro)>0:
                id_instituicao = USUARIO.objects.filter(id=usuario.id)
                USUARIO.objects.filter(cpfcnpj=cpf).update(fk_instituicao_id=id_instituicao[0].fk_instituicao_id)
                #form = AdicionarUsuarioInstituicaoForm(request.POST)
                #print (request.POST.get('cpf'))
                return render(request, 'index.html')
            else:
                messages.error(request, 'Por favor selecione um usuário existente!')
        return render(request, 'instituicao/adicionar-usuario-instituicao.html', {
            'form': form
        })
    else:
        #print('ola else')
        return render(request, 'instituicao/acesso-proibido.html')"""

''' print('cpf enviado no post = ', cpf)
    id_instituicao = USUARIO.objects.filter(id=usuario.id)
    print ('id da instituicao do usuario = ', id_instituicao[0].fk_instituicao_id)
    res_filtro = USUARIO.objects.filter(cpfcnpj=cpf)
    print('id do usuário que possui o mesmo cpf do post: ', res_filtro[0].id)
    len(res_filtro)
    print('tamanhao do vetor: ', len(res_filtro))
    #USUARIO.objects.filter(request.POST.get('cpf')==teste)
    INSTITUICAO.objects.get(id=usuario[i].fk_instituicao_id)
'''

@login_required(login_url='/accounts/login/')
def lista_patrocinar(request):
    """ Função que apresenta a tela de lista de pets a serem patrocinados"""
    usuario_lista = []
    usuario = USUARIO.objects.get(user_id = request.user.id)
    instituicao = []
    i = 0

    #adicionei esta condição encontradoPerdido=None
    pet=Pet.objects.filter(encontradoPerdido=None, adotado=False, ativo=True)

    for p in pet:
        usuario_lista.append(USUARIO.objects.get(user_id=p.user_id))
        if usuario_lista[i].fk_instituicao_id:
            instituicao.append(INSTITUICAO.objects.get(id=usuario_lista[i].fk_instituicao_id))
        i = i + 1
    lista_patrocinio = zip(pet , instituicao)
    return render(request, 'patrocinar/lista_patrocinar.html',{'pet':pet,
                                                               'usuario': usuario_lista,
                                                               'instituicao':instituicao,
                                                               'lista_patrocinio': lista_patrocinio,
                                                               'usuario': usuario                                                               
                                                               })

@login_required(login_url='/accounts/login/')
def patrocinar(request, id):
    """ Função que apresenta a tela de patrocínio """
    pet = Pet.objects.get(ativo=True, id=id)
    usuario = USUARIO.objects.get(user_id=pet.user_id)
    instituicao = INSTITUICAO.objects.get(id=usuario.fk_instituicao_id)
    return render(request, 'patrocinar/patrocinar.html',{'pet':pet,
                                                         'usuario':usuario,
                                                         'instituicao':instituicao})

@login_required(login_url='/accounts/login/')
def patrocinar_send(request, id):
    """ Função que faz o envio de patrocínio/doação """
    
    limpeza = request.POST.get('limpeza')
    alimentacao = request.POST.get('alimentacao')
    medicamentos = request.POST.get('medicamentos')
    diaria_internacao = request.POST.get('diaria_internacao')
    patrocinio = request.POST.get('patrocinio')
    
    user = request.user
    usuario = USUARIO.objects.get(user_id = user.id)
    pet = Pet.objects.get(ativo=True, id=id)
    instituicao=INSTITUICAO.objects.get(id=pet.fk_id_instituicao_id)

    if limpeza:
        print('limpeza')
        doacao_tipo = 'limpeza'
        valor = instituicao.doacao_limpeza_valor
    elif alimentacao:
        print('alimentacao')
        doacao_tipo = 'alimentacao'
        valor = instituicao.doacao_alimentacao_valor
    elif medicamentos:
        print('medicamentos')
        doacao_tipo = 'medicamentos'
        valor = instituicao.doacao_medicamentos_valor
    elif diaria_internacao:
        print('diaria_internacao')
        doacao_tipo = 'diaria_internacao'
        valor = instituicao.doacao_diaria_internacao_valor
    elif patrocinio:
        print('patrocinio')
        doacao_tipo = 'patrocinio'
        valor = instituicao.doacao_patrocinio_valor
    else:
        doacao_tipo = 'doacao_simples'
        print(request.POST.get('doacao_simples_input'))
        valor = float(request.POST.get('doacao_simples_input'))

        patrocinio = PATROCINIO(
            FK_idPet = Pet.objects.get(id=id),
            valor = valor,
            doacao_tipo = doacao_tipo,
            data = datetime.today().strftime('%Y-%m-%d')
        )
        patrocinio.save()

        patrocinio.FK_idUsuario.add(request.user)

    aviso = "Por favor, efetue sua doação. Em um prazo de até 48 horas, iremos confirmar a transação e ela poderá constar nessa página."

    pets = []
    user = request.user
    usuario = USUARIO.objects.get(user_id = user.id)
    patrocinios = PATROCINIO.objects.filter(FK_idUsuario = user, pago = True)

    for p in patrocinios:
        pets.append(Pet.objects.get(id=p.FK_idPet_id))

    lista = zip(patrocinios , pets)

    unique_pets = set(pets)

    return render(request, 'patrocinar/meus_patrocinios.html',
                  {'aviso':aviso, 'patrocinios': patrocinios, 'pets':pets, 'lista':lista, 'usuario':usuario, 'unique_pets':unique_pets})

@login_required(login_url='/accounts/login/')
def meus_patrocinios(request):

    pets = []
    user = request.user
    usuario = USUARIO.objects.get(user_id = user.id)
    patrocinios = PATROCINIO.objects.filter(FK_idUsuario = user, pago = True)

    for p in patrocinios:
        pets.append(Pet.objects.get(id=p.FK_idPet_id))

    lista = zip(patrocinios , pets)

    unique_pets = set(pets)

    return render(request, 'patrocinar/meus_patrocinios.html',
                  {'patrocinios': patrocinios, 'pets':pets, 'lista':lista, 'usuario':usuario, 'unique_pets':unique_pets})

@login_required(login_url='/accounts/login/')
def cadastrar_doacao(request):
    id_user=request.user.id
    usuario=USUARIO.objects.get(id=id_user)

    if request.method == "POST":
        if request.user.usuario.fk_instituicao:
            instance=request.user.usuario.fk_instituicao
            product = INSTITUICAO.objects.get(id=instance.id)

            form = DoacaoCadastroForm(request.POST, instance=product)
            if form.is_valid():
                form.save()

            return render(request, 'instituicao/doacao/cadastrar-doacao.html', {
            'form': form
    })
    else:
        form = DoacaoCadastroForm(instance=request.user.usuario.fk_instituicao)

        return render(request, 'instituicao/doacao/cadastrar-doacao.html', {
            'form': form,
            'usuario': usuario
    })
    
@login_required(login_url='/accounts/login/')
def listar_doacoes(request):
    """ Função que lista todas as doações à sua instituição """
    """ Acessável pelo link /doacao/lista/ """

    usuario = USUARIO.objects.get(user_id=request.user.id)
    id_inst = request.user.usuario.fk_instituicao_id

    if id_inst is not None:
        try:
            cursor = connection.cursor()
            query = '''SELECT pat.id, pet.id AS id_pet, pat.valor, pat.data, pat.publico, pat.pago, pat.doacao_tipo, pet.nome, pet.descricao, pet.foto, usr.email
                        FROM core_patrocinio as pat
                        INNER JOIN core_pet as pet ON pet.id = pat."FK_idPet_id"
						INNER JOIN "core_patrocinio_FK_idUsuario" as doador ON doador.patrocinio_id = pat.id
						INNER JOIN auth_user as usr ON doador.user_id = usr.id
                        INNER JOIN core_instituicao as instituicao ON pet.fk_id_instituicao_id = %s
                        ORDER BY pat.id'''

            # Execução da query e inserção dos dados em uma Named Tuple
            cursor.execute(query, [id_inst])
            patrocinio = namedtuplefetchall(cursor)

            return render(request, 'instituicao/doacao/listar-doacoes.html',{
                                                                            'usuario': usuario,
                                                                            'patrocinio': patrocinio
                                                                            })
        except Exception as error:
            print("Falha em ler o banco de dados.\n", error)
        finally:
            if connection:
                connection.close()

    return redirect('/doacao/lista/')

@login_required(login_url='/accounts/login/')
def doacao_alterar_privacidade(request, id):
    """ Função que altera a privacidade de uma doação (Público = True/False) """
    """ Acessável pelo link /doacao/alterar-privacidade/<id>/ """
    """ Requisitos: login, usuário da mesma instituição do pet patrocinado, usuário com admin instituição """

    patrocinio = PATROCINIO.objects.get(id=id)
    pet = Pet.objects.get(id = patrocinio.FK_idPet_id )
    usuario = USUARIO.objects.get(id = request.user.usuario.id)

    if usuario.fk_instituicao_id == pet.fk_id_instituicao_id and usuario.is_admin_instituicao:

        if patrocinio.publico == True:
            patrocinio.publico = False
        else:
            patrocinio.publico = True

        patrocinio.save()

    return redirect('/doacao/lista/')

@login_required(login_url='/accounts/login/')
def doacao_alterar_status(request, id):
    """ Função que altera o status de uma doação (Pago = True/False) """
    """ Acessável pelo link /doacao/alterar-status/<id>/ """
    """ Requisitos: login, usuário da mesma instituição do pet patrocinado, usuário com admin instituição """

    patrocinio = PATROCINIO.objects.get(id=id)
    pet = Pet.objects.get(id = patrocinio.FK_idPet_id )
    usuario = USUARIO.objects.get(id = request.user.usuario.id)

    if usuario.fk_instituicao_id == pet.fk_id_instituicao_id and usuario.is_admin_instituicao:

        if patrocinio.pago == True:
            patrocinio.pago = False
        else:
            patrocinio.pago = True

        patrocinio.save()

    return redirect('/doacao/lista/')

@login_required(login_url='/accounts/login/')
def doacao_excluir(request, id):
    """ Função que exclui uma doação """
    """ Acessável pelo link /doacao/excluir/<id>/ """
    """ Requisitos: login, usuário da mesma instituição do pet patrocinado, usuário com admin instituição """

    patrocinio = PATROCINIO.objects.get(id=id)
    pet = Pet.objects.get(id = patrocinio.FK_idPet_id )
    usuario = USUARIO.objects.get(id = request.user.usuario.id)

    if usuario.fk_instituicao_id == pet.fk_id_instituicao_id and usuario.is_admin_instituicao:

        patrocinio.delete()

    return redirect('/doacao/lista/')

def error_404(request, exception):
    return render (request, "not-found.html")