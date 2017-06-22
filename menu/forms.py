# -*- coding: utf-8 -*-
from django import forms
from .models import *


class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        fields = ('nom', 'ingredients', 'saison', 'categorie', 'recette', 'commentaire', 'lien', 'OK_invites')

        widgets = {
            'ingredients': forms.SelectMultiple(attrs={'size': 20}),
        }

    def __init__(self, *args, **kwargs):
        super(RecetteForm, self).__init__(*args, **kwargs)
        self.fields['ingredients'].queryset = Ingredient.objects.order_by('nom')


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


class SelectionRecetteForm(forms.ModelForm):
    class Meta:
        model = SelectionRecette
        fields = '__all__'

        widgets = {
            'categories': forms.SelectMultiple(attrs={'size': 15}),
            'saisons': forms.SelectMultiple(attrs={'size': 15}),
            'ingredients': forms.SelectMultiple(attrs={'size': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(SelectionRecetteForm, self).__init__(*args, **kwargs)
        self.fields['ingredients'].queryset = Ingredient.objects.order_by('nom')
