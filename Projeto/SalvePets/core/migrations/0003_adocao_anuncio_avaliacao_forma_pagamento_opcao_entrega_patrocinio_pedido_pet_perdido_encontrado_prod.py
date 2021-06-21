# Generated by Django 3.2.4 on 2021-06-21 23:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20210621_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='FORMA_PAGAMENTO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formaPagamento', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OPCAO_ENTREGA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opcaoEntrega', models.CharField(max_length=50)),
                ('prazoEntrega', models.IntegerField()),
                ('frete', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='PRODUTO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('dadosTecnicos', models.TextField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=20)),
                ('categoria', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='USUARIO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpfCnpj', models.CharField(blank=True, max_length=11, null=True)),
                ('dataNascimento', models.DateField(blank=True, null=True, verbose_name='Data de nascimento')),
                ('telefone', models.CharField(blank=True, max_length=11, null=True, verbose_name='Nº telefone')),
                ('pontuacao', models.DecimalField(decimal_places=2, max_digits=3)),
                ('FK_idLocalizacao', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.localizacao')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TOKEN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataToken', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(max_length=20)),
                ('FK_idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PET_PERDIDO_ENCONTRADO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacoes', models.TextField()),
                ('status', models.CharField(max_length=20)),
                ('data', models.DateField()),
                ('FK_idLocalizacao', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.localizacao')),
                ('FK_idPet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pet')),
            ],
        ),
        migrations.CreateModel(
            name='PEDIDO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desconto', models.DecimalField(decimal_places=2, max_digits=2)),
                ('status', models.CharField(max_length=50)),
                ('FK_idFormaPagamento', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.forma_pagamento')),
                ('FK_idLocalizacao', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.localizacao')),
                ('FK_idOpcaoEntrega', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.opcao_entrega')),
                ('FK_idProduto', models.ManyToManyField(to='core.PRODUTO')),
                ('FK_idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PATROCINIO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacoes', models.TextField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=20)),
                ('data', models.DateField()),
                ('FK_idPet', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.pet')),
                ('FK_idUsuario', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AVALIACAO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.DecimalField(decimal_places=2, max_digits=20)),
                ('comentario', models.TextField()),
                ('FK_idUsuario', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ANUNCIO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('observacoes', models.TextField()),
                ('tipo', models.CharField(max_length=50)),
                ('dataInicio', models.DateTimeField(auto_now_add=True)),
                ('dataFim', models.DateTimeField()),
                ('status', models.CharField(max_length=50)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=20)),
                ('FK_idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ADOCAO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('dataEntrada', models.DateTimeField(auto_now_add=True)),
                ('dataAdocao', models.DateTimeField()),
                ('observacao', models.TextField()),
                ('FK_idPet', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.pet')),
                ('FK_idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
