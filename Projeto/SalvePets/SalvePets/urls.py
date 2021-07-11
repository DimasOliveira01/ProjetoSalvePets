"""SalvePets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.conf.urls import i18n
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.urls import conf
from django.urls.conf import include
from core import views
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns     #imagem
from . import settings                                                          #imagem

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    #path('login/', views.login_user),
    #path('login/submit', views.submit_login),
    #path('logout/', views.logout_user),
    path('', views.index),

    path('meu-cadastro/', views.meu_cadastro, name="meu_cadastro"),
    #path('central-do-usuario/', views.central_do_usuario),
    #path('cadastro-usuario/', views.cadastro_usuario),
    path('accounts/', include("allauth.urls")),
    #path("", include("core.urls", namespace="core")),
    path('lista-pet-encontrado/',views.lista_pets_encontrados),
    path('lista-pet-perdido/',views.lista_pets_perdidos),
    path('lista-pet-usuario/',views.lista_pets_usuario),
    path('cadastro-pet/',views.cadastro_pet),
    path('pet-informacao/<id>/',views.pet_informacao),
    path('cadastro-pet/submit',views.set_pet),
    path('deletar-pet/<id>/',views.deletar_pet),

]

#imagem
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




urlpatterns += i18n_patterns (
    #path('admin/', admin.site.urls),
    #path('login/submit', views.submit_login),
    #path('logout/', views.logout_user),
    path('', views.index),
    path('accounts/', include("allauth.urls")),
)

"""
urlpatterns += i18n_patterns (
    path('', include('lang.urls', namespace='lang')),
    path('admin/', admin.site.urls),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user),
    path('', views.index),
    path('accounts/', include("allauth.urls")),
)
"""