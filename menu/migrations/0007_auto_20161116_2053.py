# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_semainerempli_numero_semaine'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceRepas',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nom', models.CharField(max_length=70)),
                ('ordre', models.IntegerField(default=0)),
                ('actif', models.BooleanField(default=True)),
                ('libre_choix', models.BooleanField(default=False)),
                ('invite', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date de creation')),
                ('categorie', models.ManyToManyField(to='menu.Categorie')),
            ],
        ),
        migrations.CreateModel(
            name='ReferenceSaison',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nom', models.CharField(max_length=15)),
            ],
        ),
        migrations.RemoveField(
            model_name='repastrouve',
            name='recette',
        ),
        migrations.RemoveField(
            model_name='repastrouve',
            name='repas',
        ),
        migrations.RemoveField(
            model_name='semainerempli',
            name='liste_repas',
        ),
        migrations.AddField(
            model_name='repas',
            name='recette',
            field=models.OneToOneField(null=True, to='menu.Recette',on_delete=models.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='repas',
            name='semaine',
            field=models.ForeignKey(null=True, to='menu.SemaineRempli',on_delete=models.DO_NOTHING),
        ),
        migrations.AlterField(
            model_name='semainerempli',
            name='numero_semaine',
            field=models.IntegerField(default=47, null=True),
        ),
        migrations.DeleteModel(
            name='RepasTrouve',
        ),
        migrations.AddField(
            model_name='referencerepas',
            name='profil',
            field=models.ForeignKey(to='menu.ReferenceSaison',on_delete=models.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='referencerepas',
            name='saison',
            field=models.ManyToManyField(to='menu.Saison'),
        ),
    ]
