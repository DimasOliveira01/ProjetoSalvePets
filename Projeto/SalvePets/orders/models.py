from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from localflavor.br.models import BRCPFField, BRPostalCodeField, BRStateField
from model_utils.models import TimeStampedModel

from products.models import Product
from core.models import User


class Order(TimeStampedModel):
    """ Modelo referente aos dados do usuário que está fazendo a compra """
    FK_iduser = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField("Nome Completo", max_length=250)
    postal_code = BRPostalCodeField("CEP")
    address = models.CharField("Endereço", max_length=250)
    number = models.CharField("Número", max_length=250)
    complement = models.CharField("Complemento", max_length=250, blank=True)
    district = models.CharField("Bairro", max_length=250)
    state = BRStateField("Estado")
    city = models.CharField("Cidade", max_length=250)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        """ seta um texto personalizado para não aparecer o texto padrão "Object ..."
        quando estiver trabalhando com o objeto no site """
        return f"Pedido {self.id}"

    def get_total_price(self):
        """ Modelo referente ao preço total da compra """
        total_cost = sum(item.get_total_price() for item in self.items.all())
        return total_cost

    def get_description(self):
        """ Modelo referente a descrição de um determinado item da compra """
        return ", ".join(
            [f"{item.quantity}x {item.product.name}" for item in self.items.all()]
        )

class Item(models.Model):
    """ Modelo referente ao item da compra """
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(settings.CART_ITEM_MAX_QUANTITY),
        ]
    )

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        """ Modelo referente ao preço total da compra """
        return self.price * self.quantity
