from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pet, USUARIO
from .forms import UserForm, UsuarioForm
from django.db import transaction
from django.shortcuts import redirect
from django.db import connection
from collections import namedtuple
from django.core import mail
from django.utils.html import strip_tags
from django.template import loader
import os
from django.utils.translation import ugettext_lazy as _

# === Funções com render simples ===

def index(request):
    #user_form = UserForm(instance=request.user)
    #usuario_form = UsuarioForm(instance=request.user.usuario)
    #cadastro_incompleto = False
    #if usuario_form.cpfCnpj == "":
    #    cadastro_incompleto = True
    #    return render(request, 'index.html', {'cadastro_incompleto', cadastro_incompleto})
    #else:
    #    return render(request, 'index.html',{'cadastro_incompleto', cadastro_incompleto})
    return render(request, 'index.html')


def sobre(request):
    return render(request, 'sobre.html')


def em_construcao(request):
    return render(request, 'emconstrucao.html')


def teste(request):
    return render(request, 'teste.html')

# ==================================

# ===      Funções gerais        ===

def lista_pets_encontrados(request):
    pet=Pet.objects.filter(encontradoPerdido='encontrado', ativo=True) #& Pet.objects.filter(ativo=True) # & encontradoPerdido='encontrado' ativo=True
    return render(request, 'listaPetsEncontrados.html',{'pet':pet})


def lista_pets_perdidos(request):
    pet=Pet.objects.filter(encontradoPerdido='perdido', ativo=True)
    return render(request, 'listaPetsPerdidos.html',{'pet':pet})


@login_required(login_url='/accounts/login')
def lista_pets_usuario(request):
    pet=Pet.objects.filter(ativo=True, user=request.user)
    return render(request, 'listaPetsUsuario.html',{'pet':pet})


@login_required(login_url='/accounts/login')
def cadastro_pet(request):
    pet_id=request.GET.get('id')
    if pet_id:
        pet=Pet.objects.get(id=pet_id)
        if pet.user == request.user:
            return render(request,'cadastroPet.html',{'pet':pet})
    return render (request, 'cadastroPet.html')


@login_required(login_url='/accounts/login')
def set_pet(request):
    nome=request.POST.get('nome')
    descricao=request.POST.get('descricao')
    dataPerdaEncontro=request.POST.get('dataPerdaEncontro')
    especie=request.POST.get('especie')
    raca=request.POST.get('raca')
    cor=request.POST.get('cor')
    porte=request.POST.get('porte')
    peso=request.POST.get('peso')
    encontradoPerdido=request.POST.get('encontradoPerdido')
    coordenada=request.POST.get('coordenada')
    foto=request.FILES.get('foto')
    user=request.user

    # Alteração de cadastro
    pet_id=request.POST.get('pet-id')
    if pet_id:
        pet=Pet.objects.get(id=pet_id)
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
            
            pet.especie=especie
            pet.save()

            if raca:
                pet.raca=raca
                pet.save()

            if cor:
                pet.cor=cor
                pet.save()

            pet.porte=porte
            pet.save()

            if peso:
                pet.peso=peso
                pet.save()

            pet.encontradoPerdido=encontradoPerdido
            pet.save()

            pet.coordenada=coordenada
            pet.save()

            if foto:
                pet.foto = foto
                pet.save()
    else:
        pet = Pet.objects.create(porte=porte, encontradoPerdido=encontradoPerdido, foto=foto, user=user, coordenada=coordenada)
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

    url = '/pet-informacao/{}/'.format(pet.id)
    os.system('aws s3 sync /home/ubuntu/ProjetoSalvePets/Projeto/SalvePets/media/pet s3://bucket-salvepets')
    return redirect(url)


@login_required(login_url='/acccounts/login')
def deletar_pet(request, id):
    pet=Pet.objects.get(id=id)
    if pet.user == request.user:
        pet.delete()
    return redirect('/lista-pet-usuario')


@login_required(login_url='/accounts/login')
def pet_informacao(request, id):
    pet = Pet.objects.get(ativo=True, id=id)
    creator = pet.user
    return render(request, 'pet.html', {'pet':pet,'creator':creator})

@login_required
@transaction.atomic
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
    })

@login_required
@transaction.atomic
def completar_cadastro(request):
    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST, instance=request.user.usuario)
        if usuario_form.is_valid():
            usuario_form.save()            
            return render(request, 'index.html')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
            usuario_form = UsuarioForm(instance=request.user.usuario)
    return render(request, 'completar-cadastro.html', {
        'usuario_form': usuario_form,
    })

def sobre(request):
    return render(request, 'sobre.html')

def em_construcao(request):
    return render(request, 'emconstrucao.html')

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def notif_pet_encontrado(id):
    try:
        # Conexão com o banco
        cursor = connection.cursor()

        # Retorna dados do pet que está sendo cadastrado agora
        pet_query = '''SELECT pet.id, pet.coordenada, pet."encontradoPerdido", usr.email, pet.foto, pet.nome
                        FROM core_pet AS pet
                        INNER JOIN auth_user AS usr on usr.id = pet.user_id
                        WHERE pet.id = %s'''
        cursor.execute(pet_query,[id])
        pet = namedtuplefetchall(cursor)
        
        # Garante que a pessoa que cadastrou um pet perdido vai receber e-mails apenas de pets encontrados próximos a região, e vise-versa.
        if pet[0].encontradoPerdido == "perdido":
            encontradoPerdido_pesquisar = "encontrado"
        else:
            encontradoPerdido_pesquisar = "perdido"

        # Query para pegar os campos para o envio do e-mail e cálculo da distância
        query = '''SELECT pet.id, pet.nome, usr.email, pet.foto, usuario."receberNotificacoes", pet.coordenada
                        FROM core_pet AS pet
                        INNER JOIN core_usuario AS usuario ON usuario.user_id = pet.user_id
                        INNER JOIN auth_user AS usr ON usr.id = usuario.user_id
                        WHERE pet."encontradoPerdido" = %s
                        ORDER BY pet.id
                        '''

        # Execução da query e inserção dos dados em uma Named Tuple
        cursor.execute(query,[encontradoPerdido_pesquisar])
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
                    cursor.execute("SELECT ST_DistanceSphere('" + pet[0].coordenada + "','" + pets[i].coordenada + "')::numeric::integer")
                    distancias.append(cursor.fetchone())
            
            # Se o cálculo retornou algo
            if distancias:
                for list in distancias:
                    for valor in list:
                        # Percorre por todas as distâncias para caso seja menor que 10km,
                        # inicia o processo de envio de e-mail                    
                        if valor <= 10000 and pets[count].receberNotificacoes == True:
                            if pet[0].encontradoPerdido == "encontrado":
                                # Passa as informações do dono do pet próximo para o envio do e-mail
                                if pet[0].email != pets[count].email:
                                    enviar_email_pet_encontrado(pet[0].id, str(pets[count].email), pet[0].foto, pet[0].nome)
                                else:
                                    print("O e-mail da pessoa que está cadastrando é igual ao que a notificação seria enviada")
                            else:
                                # Armazena em lista todos os nomes e fotos dos pets para enviar por e-mail a quem está cadastrando.
                                if pet[0].email != pets[count].email:
                                    id_list.append(pets[count].id)
                                    nome_list.append(pets[count].nome)
                                    foto_list.append(pets[count].foto)
                                else:
                                    print("O e-mail da pessoa que está cadastrando é igual ao que a notificação seria enviada")
                        else:
                            print("Pet muito distante")
                        count = count + 1
                
                if id_list and foto_list and nome_list:
                    # Envia lista de pets encontrados para quem cadastrou um pet perdido.
                    enviar_email_pet_perdido(id_list, str(pet[0].email), foto_list, nome_list)

            else:
                print("Não existem outros pets para calcular as distâncias.")
        else:
            print("Não existem pets cadastrados. É necessário pelo menos um pet perdido e um encontrado para a notificação funcionar")
    except Exception as error:
        print("Falha em ler o banco de dados.\n", error)
    finally:
        if connection:
            connection.close()


def enviar_email_pet_encontrado(id, email, foto, nome_pet):
    id = str(id)
    assunto = _("Foi encontrado um pet próximo ao local em que o seu foi perdido")
    remetente = os.environ.get("EMAIL_HOST_USER")
    destinatario = str(email)
    nome_pet = str(nome_pet)
    
    html = loader.render_to_string('emails/pet_encontrado.html', {'id': id, 'foto': foto, 'nome_pet': nome_pet})
    plain_message = strip_tags(html)

    # Envio do e-mail
    mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)
    print("E-mail enviado com sucesso")

def enviar_email_pet_perdido(id, email, foto, nome_pet):
    assunto = _("Alguns pets próximos ao seu perdido foram encontrados!")
    remetente = os.environ.get("EMAIL_HOST_USER")
    destinatario = str(email)
    
    html = loader.render_to_string('emails/pet_perdido.html', {'id': id, 'foto': foto, 'nome_pet': nome_pet})
    plain_message = strip_tags(html)

    print(id, email, foto, nome_pet)
    # Envio do e-mail
    mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)
    print("E-mail enviado com sucesso")

# ==================================
