# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0011_auto_20161206_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repas',
            name='recette',
            field=models.ForeignKey(null=True, blank=True, to='menu.Recette'),
        ),
    ]
