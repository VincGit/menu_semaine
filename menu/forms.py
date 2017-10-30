# -*- coding: utf-8 -*-
from django import forms
from .models import *


class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        fields = ('nom', 'ingredients', 'saison', 'categorie', 'recette', 'commentaire', 'lien', 'OK_invites')

        widgets = {
            'ingredients': forms.SelectMultiple(attrs={'size': 20}),
            'saison': forms.SelectMultiple(attrs={'size': 5}),
            'categorie': forms.SelectMultiple(attrs={'size': 10}),
#            'recette': forms.Textarea(attrs={'cols': 75, 'rows': 35}),
        }

    def __init__(self, *args, **kwargs):
        super(RecetteForm, self).__init__(*args, **kwargs)
        self.fields['ingredients'].queryset = Ingredient.objects.order_by('nom')


class RepasForm(forms.ModelForm):
    class Meta:
        model = Repas
        fields = ('nom', 'actif', 'libre_choix', 'invite', 'saison', 'categorie')


class RepasFormLeger(forms.ModelForm):
    """"This form defines a subset of Repas model


    It is used to give the use the choice on the three listed fields
    It defines a widget for each field
    It defines a queryset for recette so that they are ordered by alpha name order"""
    class Meta:
        model = Repas
        fields = ('saison', 'categorie', 'recette', 'libre_choix')

        widgets = {'categorie': forms.CheckboxSelectMultiple(),
                   'saison': forms.CheckboxSelectMultiple(),
                   'recette': forms.Select(),
                   'libre_choix': forms.CheckboxInput()}

    def __init__(self, *args, **kwargs):
        super(RepasFormLeger, self).__init__(*args, **kwargs)
        self.fields['recette'].queryset = Recette.objects.order_by('nom')


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
