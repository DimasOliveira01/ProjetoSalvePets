# Generated by Django 3.2.4 on 2021-06-28 00:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ABRIGO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FORMA_PAGAMENTO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formaPagamento', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LOCALIZACAO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cidade', models.CharField(max_length=50)),
                ('uf', models.CharField(max_length=2)),
                ('rua', models.CharField(max_length=200)),
                ('cep', models.CharField(max_length=10)),
                ('num', models.IntegerField()),
                ('bairro', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OPCAO_ENTREGA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opcaoEntrega', models.CharField(max_length=50)),
                ('prazoEntrega', models.IntegerField()),
                ('frete', models.DecimalField(decimal_places=15, max_digits=30)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('observacoes', models.TextField()),
                ('comprimento', models.DecimalField(decimal_places=15, max_digits=30)),
                ('largura', models.DecimalField(decimal_places=15, max_digits=30)),
                ('dataNascimento', models.DateField(blank=True, null=True)),
                ('raca', models.CharField(max_length=50)),
                ('cor', models.CharField(max_length=30)),
                ('altura', models.DecimalField(decimal_places=15, max_digits=30)),
                ('peso', models.DecimalField(decimal_places=15, max_digits=30)),
                ('FK_idAbrigo', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.abrigo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PRODUTO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('dadosTecnicos', models.TextField()),
                ('valor', models.DecimalField(decimal_places=15, max_digits=30)),
                ('categoria', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='USUARIO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpfCnpj', models.CharField(blank=True, max_length=11, null=True)),
                ('dataNascimento', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('telefone', models.CharField(blank=True, max_length=11, null=True, verbose_name='Nº telefone')),
                ('pontuacao', models.DecimalField(decimal_places=15, max_digits=30)),
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
                ('data', models.DateField(blank=True, null=True)),
                ('FK_idLocalizacao', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.localizacao')),
                ('FK_idPet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pet')),
            ],
        ),
        migrations.CreateModel(
            name='PEDIDO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desconto', models.DecimalField(decimal_places=15, max_digits=30)),
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
                ('valor', models.DecimalField(decimal_places=15, max_digits=30)),
                ('data', models.DateField(blank=True, null=True)),
                ('FK_idPet', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.pet')),
                ('FK_idUsuario', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AVALIACAO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.DecimalField(decimal_places=15, max_digits=30)),
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
                ('dataInicio', models.DateTimeField(auto_now_add=True, null=True)),
                ('dataFim', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(max_length=50)),
                ('valor', models.DecimalField(decimal_places=15, max_digits=30)),
                ('FK_idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ADOCAO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('dataEntrada', models.DateTimeField(auto_now_add=True, null=True)),
                ('dataAdocao', models.DateTimeField(blank=True, null=True)),
                ('observacao', models.TextField()),
                ('FK_idPet', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.pet')),
                ('FK_idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='abrigo',
            name='FK_idLocalizacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.localizacao'),
        ),
        migrations.AddField(
            model_name='abrigo',
            name='FK_idUsuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
