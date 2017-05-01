# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_repastrouve_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='semainerempli',
            name='numero_semaine',
            field=models.IntegerField(null=True, default=44),
        ),
    ]
