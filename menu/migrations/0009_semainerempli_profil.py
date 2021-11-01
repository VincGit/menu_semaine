# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_auto_20161116_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='semainerempli',
            name='profil',
            field=models.ForeignKey(null=True, to='menu.ReferenceSaison',on_delete=models.DO_NOTHING),
        ),
    ]
