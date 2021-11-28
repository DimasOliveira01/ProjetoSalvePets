from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from products.models import Product

from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    """ Tela com as informações de um produto incuido na compra """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product, quantity=cd["quantity"], override_quantity=cd["override"]
        )

    return redirect("cart:detail")

@require_POST
def cart_remove(request, product_id):
    """ Tela com as informações de um produto removido da compra """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:detail")

@login_required(login_url='/accounts/login')
def cart_detail(request):
    """ Tela com as informações da compra """
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})
