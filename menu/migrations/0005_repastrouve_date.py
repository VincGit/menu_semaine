# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_repastrouve_semainerempli'),
    ]

    operations = [
        migrations.AddField(
            model_name='repastrouve',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 1, 20, 58, 45, 447850, tzinfo=utc), verbose_name='Date de creation', auto_now_add=True),
            preserve_default=False,
        ),
    ]
