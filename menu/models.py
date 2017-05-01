from django.db import models
import datetime


class Categorie(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


class Saison(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


class Ingredient(models.Model):
    nom = models.CharField(max_length=70)

    def __str__(self):
        return self.nom


class Recette(models.Model):
    nom = models.CharField(max_length=170)
    recette = models.TextField(null=True, blank=True)
    lien = models.URLField(null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)
    categorie = models.ManyToManyField('Categorie')
    saison = models.ManyToManyField('Saison')
    OK_invites = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient', blank=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de creation")

    def __str__(self):
        return self.nom + self.recette


class ReferenceSaison(models.Model):
    """Cette classe permet de stocker les profils de saison
    Printemps, Ete, Autonme, Hiver, Precedent"""
    nom = models.CharField(max_length=15)

    def __str__(self):
        return self.nom


class ReferenceRepas(models.Model):
    """Cette classe permet de stocker des semaines types

    Pour chaque saison definit par ReferenceSaison on va definir une semaine
    type. On copiera ces references pour creer les vrais repas"""
    profil = models.ForeignKey('ReferenceSaison')
    nom = models.CharField(max_length=70)
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    libre_choix = models.BooleanField(default=False)
    invite = models.BooleanField(default=False)
    saison = models.ManyToManyField('Saison')
    categorie = models.ManyToManyField('Categorie')
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de creation")

    def __str__(self):
        return self.nom


class Repas(models.Model):
    """Cette classe definit un repas associe a une recette.

    Un repas est cree a partir d'un repas de reference que l'on associe ensuite
    a une recette et a une semaine"""
    nom = models.CharField(max_length=70)
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    libre_choix = models.BooleanField(default=False)
    invite = models.BooleanField(default=False)
    saison = models.ManyToManyField('Saison')
    categorie = models.ManyToManyField('Categorie')
    recette = models.ForeignKey('Recette', null=True, blank=True)
    semaine = models.ForeignKey('SemaineRempli', null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation",
                                auto_now=False)

    def __str__(self):
        if not self.recette:
            return self.nom + " pas de repas trouve "
        else:
            return self.nom + " le repas sera : " + self.recette.nom


class SemaineRempli(models.Model):
    numero_semaine = models.IntegerField(null=True,
                                         default=datetime.datetime.now().isocalendar()[1] + 1)
    profil = models.ForeignKey('ReferenceSaison', null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de creation")
