# Generated by Django 3.2.8 on 2021-11-01 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('recurring', models.BooleanField(default=False, verbose_name='Récurrent')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=170)),
                ('recette', models.TextField(blank=True, null=True)),
                ('lien', models.URLField(blank=True, null=True)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('OK_invites', models.BooleanField(default=False, verbose_name='OK invités')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('categorie', models.ManyToManyField(to='menu.Categorie', verbose_name='Catégorie')),
                ('ingredients', models.ManyToManyField(blank=True, to='menu.Ingredient', verbose_name='Ingrédients')),
            ],
        ),
        migrations.CreateModel(
            name='ReferenceSaison',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Saison',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SemaineRempli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_semaine', models.IntegerField(blank=True, default=45, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('ingredients', models.ManyToManyField(blank=True, to='menu.Ingredient', verbose_name='Ingrédient')),
                ('profil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='menu.referencesaison')),
                ('purchase_items', models.ManyToManyField(blank=True, to='menu.PurchaseItem', verbose_name='Achat')),
            ],
        ),
        migrations.CreateModel(
            name='SelectionRecette',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_present', models.BooleanField(default=False, verbose_name='Invite_present')),
                ('categories', models.ManyToManyField(blank=True, to='menu.Categorie', verbose_name='Catégories')),
                ('ingredients', models.ManyToManyField(blank=True, to='menu.Ingredient', verbose_name='Ingrédients')),
                ('saisons', models.ManyToManyField(blank=True, to='menu.Saison', verbose_name='Saisons')),
            ],
        ),
        migrations.CreateModel(
            name='Repas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=70)),
                ('ordre', models.IntegerField(default=0)),
                ('actif', models.BooleanField(default=True)),
                ('libre_choix', models.BooleanField(default=False)),
                ('invite', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('categorie', models.ManyToManyField(blank=True, to='menu.Categorie')),
                ('recette', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='menu.recette')),
                ('saison', models.ManyToManyField(blank=True, to='menu.Saison')),
                ('semaine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='menu.semainerempli')),
            ],
        ),
        migrations.CreateModel(
            name='ReferenceRepas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=70)),
                ('ordre', models.IntegerField(default=0)),
                ('actif', models.BooleanField(default=True)),
                ('libre_choix', models.BooleanField(default=False)),
                ('invite', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('categorie', models.ManyToManyField(to='menu.Categorie')),
                ('profil', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='menu.referencesaison')),
                ('saison', models.ManyToManyField(to='menu.Saison')),
            ],
        ),
        migrations.AddField(
            model_name='recette',
            name='saison',
            field=models.ManyToManyField(to='menu.Saison'),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='type',
            field=models.ManyToManyField(to='menu.PurchaseType', verbose_name="Type d'achat"),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='type',
            field=models.ManyToManyField(to='menu.PurchaseType', verbose_name="Type d'ingrédients"),
        ),
    ]
