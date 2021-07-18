from django.db.models.fields import files
from django.forms.forms import Form
from django.http import request
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Pet
from .forms import PetForm


# Create your views here.


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
    observacoes=request.POST.get('observacoes')
    #comprimento=request.POST.get('comprimento')
    #largura=request.POST.get('largura')
    dataNascimento=request.POST.get('dataNascimento')
    raca=request.POST.get('raca')
    cor=request.POST.get('cor')
    altura=request.POST.get('altura')
    peso=request.POST.get('peso')
    encontradoPerdido=request.POST.get('encontradoPerdido')
    #coordenada=request.POST.get('coordenada')
    foto=request.FILES.get('foto')
    user=request.user
    #alteração de cadastro
    pet_id=request.POST.get('pet-id')
    if pet_id:
        pet=Pet.objects.get(id=pet_id)
        if user == pet.user:
            pet.nome=nome
            pet.descricao=descricao
            pet.observacoes=observacoes
            pet.dataNascimento=dataNascimento
            pet.raca=raca
            pet.cor=cor
            pet.altura=altura
            pet.peso=peso
            pet.encontradoPerdido=encontradoPerdido
            if foto:
                pet.foto = foto
            pet.save()
            #pet.comprimento=comprimento
            #pet.largura=largura
            #pet.coordenada=coordenada
    else:
        pet = Pet.objects.create(nome=nome, descricao=descricao, observacoes=observacoes, dataNascimento=dataNascimento, raca=raca, cor=cor, altura=altura, peso=peso, encontradoPerdido=encontradoPerdido, foto=foto, user=user)    #retirei comprimento=comprimento, largura=largura, coordenada=coordenada,
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

def index(request):
    return render(request, 'index.html')
    
def localizacao(request):
    return render(request, 'localizacao.html')




"""
def logout_user(request):
    logout(request)
    #return redirect('/login/')
    return redirect('/')
"""
#def login_user(request):
 #   return render(request, 'login.html')

#def cadastro_usuario(request):
 #   return render(request, 'cadastro-usuario.html')

#tentativa de página inicial
#@login_required(login_url='/login/')
#def central_do_usuario(request):
 #   return render(request, 'central-do-usuario.html')

#final de tentativa

#@csrf_protect
#def submit_login(request):
#    if request.POST:
#        username=request.POST.get('username')
#        password=request.POST.get('password')
#        user = authenticate(username=username, password=password)
#        if user is not None:
#            login(request, user)
#            return redirect('/')            
#        else:
#            messages.error(request, 'Usuário e senha inválido. Tente novamente.')
#    return redirect('/login')
