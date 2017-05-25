# -*- coding: utf-8 -*-
from django import forms
from .models import *


class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        fields = ('nom', 'ingredients', 'saison', 'categorie', 'recette', 'commentaire', 'lien', 'OK_invites')


class RepasForm(forms.ModelForm):
    class Meta:
        model = Repas
        fields = ('nom', 'actif', 'libre_choix', 'invite', 'saison', 'categorie')


class RepasFormLeger(forms.ModelForm):
    class Meta:
        fields = ('nom', 'saison', 'categorie', 'recette')


class NumeroSemaine(forms.Form):
    numero_semaine = forms.IntegerField(required=False)


class SemaineRempli(forms.ModelForm):
    class Meta:
        model = SemaineRempli
        fields = ('numero_semaine', 'profil')
