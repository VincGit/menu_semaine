# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0009_semainerempli_profil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repas',
            name='recette',
            field=models.ForeignKey(blank=True, null=True, to='menu.Recette'),
        ),
        migrations.AlterField(
            model_name='semainerempli',
            name='numero_semaine',
            field=models.IntegerField(null=True, default=50),
        ),
    ]
