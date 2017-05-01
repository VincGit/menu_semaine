# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recette',
            name='ingredients',
            field=models.ManyToManyField(to='menu.Ingredient', null=True),
        ),
    ]
