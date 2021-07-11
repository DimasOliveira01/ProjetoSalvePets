from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Pet
from .models import USUARIO
from django import forms
from django.contrib.auth.forms import UserChangeForm
from .forms import MeuCadastroForm


# Create your views here.

#class HomePageView(TemplateView):
 #   template_name = "index.html"

@login_required(login_url='/accounts/login/')
def lista_pets_encontrados(request):
    pet=Pet.objects.filter(encontradoPerdido='encontrado') #& Pet.objects.filter(ativo=True) # & encontradoPerdido='encontrado' ativo=True
    return render(request, 'listaPets.html',{'pet':pet})

@login_required(login_url='/accounts/login/')
def lista_pets_perdidos(request):
    pet=Pet.objects.filter(encontradoPerdido='perdido')
    return render(request, 'listaPets.html',{'pet':pet})

@login_required(login_url='/accounts/login')
def lista_pets_usuario(request):
    pet=Pet.objects.filter(ativo=True, user=request.user)
    return render(request, 'listaPets.html',{'pet':pet})

def index(request):
    return render(request, 'index.html')

def cadastro_pet(request):
    return render(request, 'cadastroPet.html')

@login_required(login_url='/meu-cadastro')
def meu_cadastro(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST)
        if form.is_valid():
            #usuario=USUARIO.objects
            return render(request, 'meuCadastro.html')
    form = UserChangeForm()
    return render(request, "meuCadastro.html", {'form':form})


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
