# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0010_auto_20161206_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repas',
            name='recette',
            field=models.ForeignKey(to='menu.Recette', null=True,on_delete=models.DO_NOTHING),
        ),
    ]
