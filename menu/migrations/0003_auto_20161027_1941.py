# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20161027_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recette',
            name='ingredients',
            field=models.ManyToManyField(to='menu.Ingredient', blank=True),
        ),
    ]
