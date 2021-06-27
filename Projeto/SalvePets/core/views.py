from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView


# Create your views here.

#class HomePageView(TemplateView):
 #   template_name = "index.html"


def index(request):
    return render(request, 'index.html')

def logout_user(request):
    logout(request)
    #return redirect('/login/')
    return redirect('/')

#def login_user(request):
 #   return render(request, 'login.html')

#def cadastro_usuario(request):
 #   return render(request, 'cadastro-usuario.html')

#tentativa de página inicial
#@login_required(login_url='/login/')
#def central_do_usuario(request):
 #   return render(request, 'central-do-usuario.html')

#final de tentativa

@csrf_protect
def submit_login(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
            #return redirect('/central-do-usuario')
        else:
            messages.error(request, 'Usuário e senha inválido. Tente novamente.')
    return redirect('/login')
