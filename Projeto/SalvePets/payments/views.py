import json

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.functional import cached_property
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView
from django.core import mail
from django.utils.html import strip_tags
from django.template import loader
import os
from django.utils.translation import ugettext_lazy as _
from django.http import request

from orders.models import Order
#from orders.models import Item

from .forms import PaymentForm, UpdatePaymentForm
from .models import Payment


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm

    @cached_property
    def order(self):
        order_id = self.request.session.get("order_id")
        order = get_object_or_404(Order, id=order_id)
        return order

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["order"] = self.order
        return form_kwargs

    def form_valid(self, form):
        form.save()
        redirect_url = "payments:failure"
        status = form.instance.mercado_pago_status

        if status == "approved":
            redirect_url = "payments:success"
            
            order_id = self.request.session.get("order_id")
            order = get_object_or_404(Order, id=order_id)
            #itens = get_object_or_404(Item, id=order_id)

            email = self.request.user.email
            #id = str(id)
            assunto = _("Pedido Recebido!")
            remetente = os.environ.get("EMAIL_HOST_USER")
            destinatario = str(email)            
            #html = loader.render_to_string('emails/pet_encontrado.html', {'id': id, 'foto': foto, 'nome_pet': nome_pet})
            html = loader.render_to_string('emailPedido.html', {'id':order_id, 'order': order, 'price': order.get_total_price, 'nome': order.name, 'cep':order.postal_code, 'endereco':order.address,'cidade': order.city, 'estado': order.state, 'bairro': order.district,'numero': order.number,'complemento': order.complement})
            plain_message = strip_tags(html)

            # Envio do e-mail
            mail.send_mail(assunto, plain_message, remetente, [destinatario], html_message=html)

        if status == "in_process":
            redirect_url = "payments:pending"

        if status and status != "rejected":
            del self.request.session["order_id"]
        return redirect(redirect_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.order
        context["publishable_key"] = settings.MERCADO_PAGO_PUBLIC_KEY
        return context


class PaymentFailureView(TemplateView):
    template_name = "payments/failure.html"


class PaymentPendingView(TemplateView):
    template_name = "payments/pending.html"

class PaymentSuccessView(TemplateView):
    template_name = "payments/success.html"           

@csrf_exempt
@require_POST
def payment_webhook(request):
    data = json.loads(request.body)
    form = UpdatePaymentForm(data)
    if form.is_valid():
        form.save()

    return JsonResponse({})


