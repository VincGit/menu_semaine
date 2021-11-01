# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20161027_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepasTrouve',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recette_libre', models.BooleanField(default=False)),
                ('recette', models.ForeignKey(to='menu.Recette', null=True,on_delete=models.DO_NOTHING)),
                ('repas', models.ForeignKey(to='menu.Repas',on_delete=models.DO_NOTHING)),
            ],
        ),
        migrations.CreateModel(
            name='SemaineRempli',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date de creation')),
                ('liste_repas', models.ManyToManyField(to='menu.RepasTrouve')),
            ],
        ),
    ]
