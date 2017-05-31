# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    #gestion du menu de la semaine
    url(r'^generer_semaine/', views.generer_semaine, name="generer_semaine"),
    url(r'^generer_menu/$', views.generer_menu, name="generer_menu"),
    url(r'^voir_semaines_precedentes/', views.liste_semaines_precedentes,
        name="liste_semaines_precedentes"),
    url(r'^voir_semaine/(?P<semaine_id>\d+)', views.voir_semaine,
        name="voir_semaine"),
    url(r'^editer_profil_semaine', views.editer_profil_semaine,
        name="editer_profil_semaine"),
    url(r'^modifier_menu/(?P<form_id>\d+)', views.menu_modifier,
        name="menu_modifier"),
    url(r'^reediter_menu_semaine/', views.reediter_menu_semaine,
        name="reediter_menu_semaine"),
    #gestion des recettes
    url(r'^liste$', views.liste_recette, name="liste_recette"),
    url(r'^recette/(?P<id>\d+)', views.voir_detail, name="voir_detail"),
    url(r'^entrer_recette/', views.entrer_recette, name="entrer_recette"),
    url(r'^editer_recette/(?P<id>\d+)', views.editer_recette,
        name="editer_recette"),
    url(r'^recette', views.recette_aleatoire, name="recette_aleatoire"),
        ]