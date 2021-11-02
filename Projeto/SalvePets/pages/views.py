from django.shortcuts import render

from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "products/product_list.html"