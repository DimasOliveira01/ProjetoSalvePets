from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import Item, Order


class OrderCreateView(CreateView):
    """ Cria a tela de compra de produtos """
    model = Order
    form_class = OrderCreateForm

    def form_valid(self, form):
        cart = Cart(self.request)
        if cart:
            order = form.save()

            usuario = self.request.user

            Order.objects.filter(id=order.id).update(FK_iduser=usuario.id)

            for item in cart:
                Item.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            #cart.clear()
            self.request.session["order_id"] = order.id

            return redirect(reverse("payments:process"))
        return redirect(reverse("pages:home_ecommerce"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        return context
