from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PATROCINIO, Pet, USUARIO, INSTITUICAO
from .forms import UserForm, UsuarioForm, InstituicaoForm, AdicionarUsuarioInstituicaoForm, AdicionarPetInstituicao, SolicitarAdocaoForm
from django.db import transaction
from django.shortcuts import redirect
from django.db import connection
from collections import namedtuple
from django.core import mail
from django.utils.html import strip_tags
from django.template import loader
import os
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from datetime import timedelta


from .forms import ContactForm
from django.core.mail import message, send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings

# === Funções com render simples ===

def index(request):
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
    return render(request, 'sobre.html')


def em_construcao(request):
    return render(request, 'emconstrucao.html')

def faq(request):
    return render(request, 'faq.html')



# ==================================

# ===      Funções gerais        ===

def lista_pets_encontrados(request):
    pet=Pet.objects.filter(encontradoPerdido='Encontrado', ativo=True) #& Pet.objects.filter(ativo=True) # & encontradoPerdido='encontrado' ativo=True
    return render(request, 'listaPetsEncontrados.html',{'pet':pet})


def lista_pets_perdidos(request):
    pet=Pet.objects.filter(encontradoPerdido='Perdido', ativo=True)
    return render(request, 'listaPetsPerdidos.html',{'pet':pet})


@login_required(login_url='/accounts/login')
def lista_pets_usuario(request):
    pet=Pet.objects.filter(ativo=True, user=request.user,fk_id_instituicao=None)
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
    sexo=request.POST.get('sexo')
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
        
        # Tamanho máximo de arquivo
        if foto:
            MAX_SIZE = 2097152
            file = request.FILES['foto']
            extensao = os.path.splitext(file.name)[1]
            extensao_valida = ['.png', '.jpg', '.jpeg', '.bmp']

            if not extensao in extensao_valida:
                return redirect('/cadastro-pet/?id={}'.format(pet.id))

            if file.size > MAX_SIZE:
                return redirect('/cadastro-pet/?id={}'.format(pet.id))

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
    else:
        if foto:
            MAX_SIZE = 2097152
            file = request.FILES['foto']
            extensao = os.path.splitext(file.name)[1]
            print(extensao)
            extensao_valida = ['.png', '.jpg', '.jpeg', '.bmp']

            if not extensao in extensao_valida:
                erro = "Os formatos de imagem permitidos são PNG, JPG, JPEG e BMP."
                return render(request, 'cadastroPet.html', {'erro': erro})

            if file.size > MAX_SIZE:
                erro = "O tamanho da imagem deve ser menor que 2 MB"
                return render(request, 'cadastroPet.html', {'erro': erro})

        pet = Pet.objects.create(porte=porte, encontradoPerdido=encontradoPerdido, foto=foto, user=user, coordenada=coordenada, sexo=sexo)
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
    return redirect(url)


@login_required(login_url='/acccounts/login')
def deletar_pet(request, id):
    pet=Pet.objects.get(id=id)
    if pet.user == request.user:
        pet.delete()
    return redirect('/lista-pet-usuario')


#@login_required(login_url='/accounts/login')
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
    try:
        # Conexão com o banco
        cursor = connection.cursor()

        # Retorna dados do pet que está sendo cadastrado agora
        pet_query = '''SELECT pet.id, pet.coordenada, pet."encontradoPerdido", usr.email, pet.foto, pet.nome, pet."dataPerdaEncontro", pet.especie, pet.porte
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

        if pet[0].dataPerdaEncontro:
            perdido_inicio = pet[0].dataPerdaEncontro - timedelta(days = 60)
            perdido_fim = pet[0].dataPerdaEncontro + timedelta(days = 60)
        else:
            perdido_inicio = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
            perdido_fim = datetime.strptime('2100-01-01', '%Y-%m-%d').date()

        # Query para pegar os campos para o envio do e-mail e cálculo da distância
        query = '''SELECT pet.id, pet.nome, usr.email, pet.foto, usuario."receberNotificacoes", pet.coordenada
                        FROM core_pet AS pet
                        INNER JOIN core_usuario AS usuario ON usuario.user_id = pet.user_id
                        INNER JOIN auth_user AS usr ON usr.id = usuario.user_id
                        WHERE pet."encontradoPerdido" = %s AND pet."dataPerdaEncontro" BETWEEN %s AND %s
                            AND pet.especie = %s AND pet.porte BETWEEN %s and %s
                        ORDER BY pet.id
                        '''

        # Execução da query e inserção dos dados em uma Named Tuple
        cursor.execute(query,[encontradoPerdido_pesquisar, perdido_inicio, perdido_fim, pet[0].especie, pet[0].porte - 30, pet[0].porte + 30 ])
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
                                # Armazena em lista todos os nomes e fotos dos pets para enviar por e-mail a quem está cadastrando.
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
    id = str(id)
    assunto = _("Encontramos um pet semelhante ao seu")
    remetente = os.environ.get("EMAIL_HOST_USER")
    destinatario = str(email)
    nome_pet = str(nome_pet)
    
    html = loader.render_to_string('emails/pet_encontrado.html', {'id': id, 'foto': foto, 'nome_pet': nome_pet})
    plain_message = strip_tags(html)

    # Envio do e-mail
    mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)

def enviar_email_pet_perdido(id, email, foto, nome_pet):
    assunto = _("Novos pets parecidos com o seu foram encontrados")
    remetente = os.environ.get("EMAIL_HOST_USER")
    destinatario = str(email)
    
    html = loader.render_to_string('emails/pet_perdido.html', {'id': id, 'foto': foto, 'nome_pet': nome_pet})
    plain_message = strip_tags(html)

    # Envio do e-mail
    mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)

# ==================================
#Funções Projeto Integrado II

#Formulário para solicitar cadastro de Instituição

def cadastro_empresa(request):
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
				send_mail(subject, message, settings.EMAIL_HOST_USER, ['atendimentoSalvePets@gmail.com'],
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
    if request.method == "POST":
        if request.user.usuario.fk_instituicao:

            instance=request.user.usuario.fk_instituicao
            product = INSTITUICAO.objects.get(id=instance.id)

            form = InstituicaoForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return render(request, 'index.html')
        else:
            form = InstituicaoForm(request.POST)
            if form.is_valid():
                instancia = form.save()
                usuario = request.user.usuario
                USUARIO.objects.filter(id=usuario.id).update(fk_instituicao_id=instancia.id)
                return render(request, 'index.html')
            else:
                messages.error(request, ('Por favor corriga o erro abaixo!'))
    else:
        form = InstituicaoForm(instance=request.user.usuario.fk_instituicao)
    id_user=request.user.id
    usuario=USUARIO.objects.get(id=id_user)
    return render(request, 'instituicao/modificar-cadastro-instituicao.html', {
        'form': form, 'usuario':usuario
    })

'''
pet=Pet.objects.filter(encontradoPerdido='Encontrado', ativo=True)
instituicao=INSTITUICAO.objects.filter(encontradoPerdido='Encontrado', ativo=True)
'''

def teste(request):
    return render(request, 'teste.html')
 
def adotar(request):
    return render(request, 'adotar/cadastro_adotar.html')

@login_required
@transaction.atomic
def adicionar_usuario_instituicao(request):
    if (request.user.usuario.is_admin_instituicao == True):
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
        id_user=request.user.id
        usuario=USUARIO.objects.get(id=id_user)
        return render(request, 'instituicao/adicionar-usuario-instituicao.html', {
            'form': form, 'usuario': usuario
        })
    else:
        user=request.user.usuario
        return render(request, 'instituicao/acesso-proibido.html',{'user':user})

@login_required
@transaction.atomic
def listar_usuario_instituicao(request):
    if(request.user.usuario.is_admin_instituicao == True):
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
        return render(request, 'instituicao/listar-usuario-instituicao.html',{'usuario':usuario, 'usuario1': usuario1})
    else:
       return render(request, 'instituicao/acesso-proibido.html') 

@login_required(login_url='/acccounts/login')
@transaction.atomic
def deletar_usuario_instituicao(request, id):
    USUARIO.objects.filter(id=id).update(fk_instituicao_id=None)
    return redirect('/listar-usuario-instituicao/')

@login_required(login_url='/accounts/login')
def cadastro_pet_instituicao(request):
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
    if(request.user.usuario.fk_instituicao_id != None and existe_admin==1):
        pet_id=request.GET.get('id')
        if pet_id:
            pet=Pet.objects.get(id=pet_id)
            if pet.user == request.user:
                return render(request,'instituicao/cadastro-pet-instituicao.html',{'pet':pet,'usuario': usuario})
        return render (request, 'instituicao/cadastro-pet-instituicao.html',{'usuario': usuario})
    else:
        return render(request, 'instituicao/acesso-proibido.html')

@login_required(login_url='/acccounts/login')
def set_pet_instituicao(request):
    nome=request.POST.get('nome')
    ativo=request.POST.get('ativo')
    descricao=request.POST.get('descricao')
    especie=request.POST.get('especie')
    raca=request.POST.get('raca')
    sexo=request.POST.get('sexo')
    porte=request.POST.get('porte')
    foto=request.FILES.get('foto')
    user=request.user
    fk_id_instituicao_id=request.user.usuario.fk_instituicao_id

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

            if ativo=='on':
                pet.ativo=True
                pet.save()
            else:
                pet.ativo=False 
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
    else:
        if ativo=='on':
            ativo=True
        else:
            ativo=False
        
        pet = Pet.objects.create(ativo=ativo, porte=porte, foto=foto, user=user, sexo=sexo, fk_id_instituicao_id=fk_id_instituicao_id)
        if nome:
            pet.nome=nome
        else:
            pet.nome="Sem nome"
            pet.save()

        if ativo:
            pet.ativo=ativo
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

    url = '/pet-informacao-instituicao/{}/'.format(pet.id)
    return redirect (url)

@login_required(login_url='/accounts/login')
def pet_informacao_instituicao(request, id):
    pet = Pet.objects.get(id=id)
    inst=INSTITUICAO.objects.get(id=pet.fk_id_instituicao_id)
    id_user=request.user.id
    usuario=USUARIO.objects.get(id=id_user)
    print(id_user)
    print(inst.nome_instituicao)
    return render(request, 'instituicao/pet-instituicao.html', {'pet':pet,'inst':inst,'usuario':usuario})


def pet_informacao_instituicao_adocao(request, id):
    pet = Pet.objects.get(ativo=True, id=id)
    inst=INSTITUICAO.objects.get(id=pet.fk_id_instituicao_id)
    #id_user=request.user.id
    #print(id_user)
    #print(inst.nome_instituicao)
    return render(request, 'instituicao/pet-instituicao-adocao.html', {'pet':pet,'inst':inst})

def lista_pets_instituicao(request):
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
    if(request.user.usuario.fk_instituicao_id != None  and existe_admin==1):
        id_instituicao_usuario=request.user.usuario.fk_instituicao_id
        pet=Pet.objects.filter(encontradoPerdido=None, fk_id_instituicao_id=id_instituicao_usuario)
        id_user=request.user.id
        usuario=USUARIO.objects.get(id=id_user)
        return render(request, 'instituicao/lista-pets-instituicao.html',{'pet':pet, 'usuario': usuario})
    else:
        return render(request, 'instituicao/acesso-proibido-lista-pet.html')

def lista_pets_adocao(request):
    pet=Pet.objects.filter(encontradoPerdido=None, ativo=True)
    return render(request, 'instituicao/lista-pet-adocao.html',{'pet':pet})

#conferir esta função, mas acho que precisa retirar
@login_required(login_url='/accounts/login')
def lista_pets_usuario_instituicao(request):
    pet=Pet.objects.filter(ativo=True, user=request.user)
    return render(request, 'listaPetsUsuario.html',{'pet':pet})

@login_required(login_url='/acccounts/login')
def deletar_pet_instituicao(request, id):
    pet=Pet.objects.get(id=id)
    if pet.user == request.user:
        pet.delete()
    return redirect('/lista-pet-instituicao/')

@login_required(login_url='/acccounts/login')
def administrativo_instituicao(request):
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
            body = {'nome': form.cleaned_data['nome'], 'numero_celular': form.cleaned_data['numero_celular'], 'email': form.cleaned_data['email'],}
            message = '\n'.join(body.values())
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, ['COLOCAR EMAIL DA INSTITUICAO'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return render(request, "index.html")
    form = SolicitarAdocaoForm()
    return render(request, 'instituicao/solicitar-adocao.html', {'form':form})
'''
@login_required
def solicitar_adocao(request, id):
    user = request.user
    pet=Pet.objects.get(id=id)
    instituicao= INSTITUICAO.objects.filter(id=pet.fk_id_instituicao_id)
    subject = "Solicitação de adoção de Pet"
    body = {'Código do Pet': id, 'nome': user.first_name, 'numero_celular': user.usuario.telefone, 'email': user.email}
    message = '\n'.join(body.values())
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instituicao[0].email], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found')
    return render(request, "instituicao/solicitar-adocao.html")

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
'''

def lista_patrocinar(request):
    usuario = []
    instituicao = []
    i = 0

    pet=Pet.objects.filter(ativo=True)
    for p in pet:
        usuario.append(USUARIO.objects.get(user_id=p.user_id))
        if usuario[i].fk_instituicao_id:
            instituicao.append(INSTITUICAO.objects.get(id=usuario[i].fk_instituicao_id))
        i = i + 1
    lista_patrocinio = zip(pet , instituicao)
    return render(request, 'patrocinar/lista_patrocinar.html',{'pet':pet, 'usuario': usuario, 'instituicao':instituicao, 'lista_patrocinio': lista_patrocinio})

@login_required(login_url='/accounts/login/')
def patrocinar(request, id):
    pet = Pet.objects.get(ativo=True, id=id)
    usuario = USUARIO.objects.get(user_id=pet.user_id)
    instituicao = INSTITUICAO.objects.get(id=usuario.fk_instituicao_id)
    return render(request, 'patrocinar/patrocinar.html',{'pet':pet, 'usuario':usuario, 'instituicao':instituicao})

def patrocinar_send(request, id):

    user = request.user
    valor = float(request.POST.get('valor'))
    patrocinio_existe = PATROCINIO.objects.filter(FK_idUsuario = user, FK_idPet = Pet.objects.get(id=id))

    # TERMINAR 

    patrocinio = PATROCINIO(
        FK_idPet = Pet.objects.get(id=id),
        valor = valor,
        data = datetime.today().strftime('%Y-%m-%d')
    )
    patrocinio.save()

    patrocinio.FK_idUsuario.add(request.user)

    if valor == 20:
        destino = 'https://pag.ae/7XDvbF6CG/button'
    elif valor == 50:
        destino = 'https://pag.ae/7XDvnBuw4/button'
    elif valor == 100:
        destino = 'https://pag.ae/7XDvnLTsK/button'
    else:
        destino = '/meus-patrocinios/'

    aviso = "Por favor, efetue sua doação. Em um prazo de até 48 horas, iremos confirmar a transação e ela poderá constar nessa página."

    if valor != 0:
        return redirect(destino)
    else:
        pets = []
        patrocinios = PATROCINIO.objects.get(FK_idUsuario = user, pago = True)

        for p in patrocinios:
            pets.append(Pet.objects.get(id=p.FK_idPet_id))

        lista = zip(patrocinios , pets)
        return render(request, 'patrocinar/meus_patrocinios.html',{'aviso':aviso, 'patrocinios': patrocinios, 'pets':pets, 'lista':lista})

@login_required(login_url='/accounts/login/')
def meus_patrocinios(request):

    pets = []
    user = request.user
    patrocinios = PATROCINIO.objects.filter(FK_idUsuario = user, pago = True)

    for p in patrocinios:
        pets.append(Pet.objects.get(id=p.FK_idPet_id))

    lista = zip(patrocinios , pets)

    return render(request, 'patrocinar/meus_patrocinios.html', {'patrocinios': patrocinios, 'pets':pets, 'lista':lista})

