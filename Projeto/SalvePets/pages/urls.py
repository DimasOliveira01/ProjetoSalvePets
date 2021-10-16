from django.urls import path

#from .views import AboutPageView, HomePageView
from .views import HomePageView

app_name = "pages"

urlpatterns = [
    #path("sobre/", AboutPageView.as_view(), name="about"),
    path("ecommerce/", HomePageView.as_view(), name="home_ecommerce"),
]