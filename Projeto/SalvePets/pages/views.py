from django.shortcuts import render

from django.views.generic import TemplateView


class HomePageView(TemplateView):
    #template_name = "home_ecommerce.html"
    template_name = "products/product_list.html"


#class AboutPageView(TemplateView):
#    template_name = "sobre.html"