from django.db import models
import datetime


class Categorie(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


class PurchaseType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Saison(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


class Ingredient(models.Model):
    nom = models.CharField(max_length=70)
    type = models.ManyToManyField('PurchaseType', verbose_name="Type d'ingrédients")

    def __str__(self):
        return self.nom


class PurchaseItem(models.Model):
    name = models.CharField(max_length=70)
    type = models.ManyToManyField('PurchaseType', verbose_name="Type d'achat")
    recurring = models.BooleanField(default=False, verbose_name="Récurrent")

    def __str__(self):
        return self.name


class Recette(models.Model):
    nom = models.CharField(max_length=170)
    recette = models.TextField(null=True, blank=True)
    lien = models.URLField(null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)
    categorie = models.ManyToManyField('Categorie', verbose_name="Catégorie")
    saison = models.ManyToManyField('Saison')
    OK_invites = models.BooleanField(default=False, verbose_name="OK invités")
    ingredients = models.ManyToManyField('Ingredient', blank=True, verbose_name="Ingrédients")
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de création")

    def __str__(self):
        return self.nom


class SelectionRecette(models.Model):
    categories = models.ManyToManyField('Categorie', verbose_name="Catégories", blank=True)
    saisons = models.ManyToManyField('Saison', blank=True, verbose_name="Saisons")
    ingredients = models.ManyToManyField('Ingredient', blank=True, verbose_name="Ingrédients")
    invite_present = models.BooleanField(default=False, verbose_name="Invités")


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
    profil = models.ForeignKey('ReferenceSaison',
        on_delete=models.DO_NOTHING)
    nom = models.CharField(max_length=70)
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    libre_choix = models.BooleanField(default=False)
    invite = models.BooleanField(default=False)
    saison = models.ManyToManyField('Saison')
    categorie = models.ManyToManyField('Categorie')
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de création")

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
    saison = models.ManyToManyField('Saison', blank=True)
    categorie = models.ManyToManyField('Categorie', blank=True)
    recette = models.ForeignKey('Recette', null=True, blank=True, on_delete=models.DO_NOTHING)
    semaine = models.ForeignKey('SemaineRempli', null=True, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création",
                                auto_now=False)

    def __str__(self):
        if not self.recette:
            return self.nom + " pas de repas trouve "
        else:
            return self.nom + " le repas sera : " + self.recette.nom


class SemaineRempli(models.Model):
    numero_semaine = models.IntegerField(null=True, blank=True, default=datetime.datetime.now().isocalendar()[1] + 1)
    profil = models.ForeignKey('ReferenceSaison', null=True, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de création")
    purchase_items = models.ManyToManyField('PurchaseItem', verbose_name="Achat", blank=True)
    ingredients = models.ManyToManyField('Ingredient', verbose_name="Ingrédient", blank=True)


class NecessaryIngredient():
    def __init__(self, name, recipe_name):
        self.name = name
        self.occurrence = 1
        self.recipe_names = [recipe_name]

    def __str__(self):
        return "L'ingredient {} est utilise {} fois".format(self.name, self.occurrence)