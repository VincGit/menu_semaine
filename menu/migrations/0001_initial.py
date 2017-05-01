# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nom', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nom', models.CharField(max_length=170)),
                ('recette', models.TextField(null=True, blank=True)),
                ('lien', models.URLField(null=True, blank=True)),
                ('commentaire', models.TextField(null=True, blank=True)),
                ('OK_invites', models.BooleanField(default=False)),
                ('date', models.DateTimeField(verbose_name='Date de creation', auto_now_add=True)),
                ('categorie', models.ManyToManyField(to='menu.Categorie')),
                ('ingredients', models.ManyToManyField(to='menu.Ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Repas',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nom', models.CharField(max_length=70)),
                ('ordre', models.IntegerField(default=0)),
                ('actif', models.BooleanField(default=True)),
                ('libre_choix', models.BooleanField(default=False)),
                ('invite', models.BooleanField(default=False)),
                ('date', models.DateTimeField(verbose_name='Date de creation', auto_now_add=True)),
                ('categorie', models.ManyToManyField(to='menu.Categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Saison',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='repas',
            name='saison',
            field=models.ManyToManyField(to='menu.Saison'),
        ),
        migrations.AddField(
            model_name='recette',
            name='saison',
            field=models.ManyToManyField(to='menu.Saison'),
        ),
    ]
