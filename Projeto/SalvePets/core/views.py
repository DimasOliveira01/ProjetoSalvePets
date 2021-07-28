from django.db.models.fields import files
from django.forms.forms import Form
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Pet, USUARIO
from .models import User
from .forms import PetForm, UserForm, UsuarioForm
from django.db import transaction
from django.shortcuts import redirect

#from geopy.geocoders import Nominatim

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
    coordenada=request.POST.get('coordenada')
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
            pet.coordenada=coordenada
            if foto:
                pet.foto = foto
            pet.save()
            #pet.comprimento=comprimento
            #pet.largura=largura
            #pet.coordenada=coordenada
    else:
        pet = Pet.objects.create(nome=nome, descricao=descricao, observacoes=observacoes, dataNascimento=dataNascimento, raca=raca, cor=cor, altura=altura, peso=peso, encontradoPerdido=encontradoPerdido, foto=foto, user=user, coordenada=coordenada)    #retirei comprimento=comprimento, largura=largura, coordenada=coordenada,
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

def sobre(request):
    return render(request, 'sobre.html')