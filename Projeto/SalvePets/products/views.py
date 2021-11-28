from django.db.models.expressions import Value
from django.http import request
from cart.forms import CartAddProductForm
from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Category, Product


class ProductDetailView(DetailView):
    queryset = Product.available.all()
    extra_context = {"form": CartAddProductForm()}


class ProductListView(ListView):
    category = None
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.available.all()
        #queryset = queryset.order_by('price')
        # 
        #filtro_preco = self.request.GET.get('filtro_preco')     
        #if filtro_preco:
        #    if COMO PEGAR O VALUE DO SELECT DA TEMPLATE?
        #       queryset = queryset.order_by('price') #ORDENA A LISTA DE PRODUTOS

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        category_slug = self.kwargs.get("slug")
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)

            search = self.request.GET.get('search')
            if search:
                queryset = queryset.filter(name__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["categories"] = Category.objects.all()
        return context