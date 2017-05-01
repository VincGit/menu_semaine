# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('menu.views',
    #gestion du menu de la semaine
    url(r'^menu/generer_semaine/$', 'generer_semaine', name="generer_semaine"),
    url(r'^generer_menu/$', 'generer_menu', name="generer_menu"),
    url(r'^voir_semaines_precedentes/$', 'liste_semaines_precedentes',
        name="liste_semaines_precedentes"),
    url(r'^voir_semaine/(?P<semaine_id>\d+)$', 'voir_semaine',
        name="voir_semaine"),
    url(r'^editer_profil_semaine$', 'editer_profil_semaine',
        name="editer_profil_semaine"),
    url(r'modifier_menu/(?P<form_id>\d+)$', 'menu_modifier',
        name="menu_modifier"),
    url(r'reediter_menu_semaine/$', 'reediter_menu_semaine',
        name="reediter_menu_semaine"),
    #gestion des recettes
    url(r'^liste$', 'liste_recette', name="liste_recette"),
    url(r'^recette/(?P<id>\d+)$', 'voir_detail', name="voir_detail"),
    url(r'^entrer_recette/$', 'entrer_recette', name="entrer_recette"),
    url(r'^editer_recette/(?P<id>\d+)$', 'editer_recette',
        name="editer_recette"),
    url(r'^recette$', 'recette_aleatoire', name="recette_aleatoire"),
        )