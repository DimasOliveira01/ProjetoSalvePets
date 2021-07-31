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

# === Funções com render simples ===

def index(request):
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
    return render(request, 'listaPets.html',{'pet':pet})


def lista_pets_perdidos(request):
    pet=Pet.objects.filter(encontradoPerdido='perdido', ativo=True)
    return render(request, 'listaPets.html',{'pet':pet})


@login_required(login_url='/accounts/login')
def lista_pets_usuario(request):
    pet=Pet.objects.filter(ativo=True, user=request.user)
    return render(request, 'listaPets.html',{'pet':pet})


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
    dataNascimento=request.POST.get('dataNascimento')
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
            pet.nome=nome
            pet.descricao=descricao
            pet.dataNascimento=dataNascimento
            pet.raca=raca
            pet.cor=cor
            pet.porte=porte
            pet.peso=peso
            pet.encontradoPerdido=encontradoPerdido         
            pet.coordenada=coordenada
            if foto:
                pet.foto = foto
            pet.save()
    else:
        pet = Pet.objects.create(nome=nome, porte=porte, encontradoPerdido=encontradoPerdido, foto=foto, user=user)
        if descricao:
            pet.descricao = descricao
            pet.save()
        if dataNascimento:
            pet.dataNascimento = dataNascimento
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

    url = '/pet-informacao/{}/'.format(pet.id)
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
    return render(request, 'pet.html', {'pet':pet})


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


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def localizacao(request):
    if request.method == "GET":
        try:
            # Conexão com o banco
            cursor = connection.cursor()
            
            # Query para pegar os campos para o envio do e-mail e cálculo da distância
            query = '''SELECT pet.id, pet.nome, usr.email, pet.foto, usuario."receberNotificacoes", pet.coordenada
	                        FROM core_pet AS pet
	                        INNER JOIN core_usuario AS usuario ON usuario.user_id = pet.user_id
	                        INNER JOIN auth_user AS usr ON usr.id = usuario.user_id
                            ORDER BY pet.id
                            '''

            # Execução da query e inserção dos dados em uma Named Tuple
            cursor.execute(query)
            pets = namedtuplefetchall(cursor)

            # Caso existam pets no banco de dados
            if pets:
                distancias = []
                count = 0
                varios_pets = {}

                # Calcula distância desse pet cadastrado com todos os outros no banco de dados
                for i in range(len(pets) - 1):
                    cursor.execute("SELECT ST_DistanceSphere('" + pets[0].coordenada + "','" + pets[i+1].coordenada + "')::numeric::integer")
                    distancias.append(cursor.fetchone())

                if distancias:
                    for list in distancias:
                        for valor in list:
                            # Percorre por todas as distâncias para caso seja menor que 10km,
                            # inicia o processo de envio de e-mail                    
                            if valor <= 10000 and pets[count].receberNotificacoes == True:
                                id = pets[count].id
                                email = str(pets[count].email)
                                foto = pets[count].foto
                                nome_pet = pets[count].nome

                                # Passa as informações do dono do pet próximo para o envio do e-mail
                                enviar_email_pet(id, email, foto, nome_pet)

                            count = count + 1
                else:
                    print("Não existem outros pets para calcular as distâncias.")
            else:
                print("Não existem pets cadastrados.")
        
            return render(request, 'localizacao.html')

        except Exception as error:
            print("Falha em ler o banco de dados.\n", error)
            return render(request, 'localizacao.html')
        finally:
            if connection:
                connection.close()


def enviar_email_pet(id, email, foto, nome_pet):
    id = str(id)
    assunto = "Seu pet foi encontrado!"
    remetente = "atendimentoSalvePets@gmail.com"
    destinatario = str(email)
    nome_pet = str(nome_pet)
    
    html = loader.render_to_string('emails/pet_encontrado.html', {'id': id, 'foto': foto, 'nome_pet': nome_pet})
    plain_message = strip_tags(html)

    # Envio do e-mail
    mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)

# ==================================