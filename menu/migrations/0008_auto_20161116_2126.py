# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_auto_20161116_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repas',
            name='recette',
            field=models.ForeignKey(to='menu.Recette', null=True),
        ),
    ]
