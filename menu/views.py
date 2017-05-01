import random
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.forms import modelformset_factory
from . import forms
from . import models


def editer_recette(request, id):
    recette = get_object_or_404(models.Recette, id=id)

    if request.method == 'POST':  # S'il s'agit d'une requête POST
        print("C'est un post'")
        # Nous reprenons les données
        form = forms.RecetteForm(request.POST, instance=recette)
        if form.is_valid():  # Nous vérifions que les données sont valides
            print("Forme est valide")
            form.save()
            return redirect('voir_detail', id=id)
    else:  # Si ce n'est pas du POST, c'est probablement une requête GET
        form = forms.RecetteForm(instance=recette)

    return render(request, 'menu/editer_recette.html', {'form': form, 'id':
        recette.id})


def generer_semaine(request):
    if request.method == 'POST':
        semaine_id = request.session.get('semaine_id')
        if semaine_id:
            semaine = models.SemaineRempli.objects.get(id=semaine_id)
            # On modifie la semaine avec les donnees recuperees
            form = forms.SemaineRempli(request.POST, instance=semaine)
            if form.is_valid():
                # numero_semaine = form.cleaned_data['numero_semaine']
                # print(numero_semaine)
                # if verifier_semaine_duplique(request, numero_semaine):
                # return render(request, 'menu/generer_nouvelle_semaine.html',
                # {"form_semaine": form})
                # if form.is_valid():
                form.save()
                # on recupere une reference de repas (ete, automne, ...)
                # et on creer un repas en fonction de ca
                # TODO
                print(form.cleaned_data['profil'])
                reference_saison = models.ReferenceSaison.objects.filter(nom=
                                                                         form.cleaned_data['profil'])
                liste_reference_repas = models.ReferenceRepas.objects.filter(
                    profil=reference_saison)

                # TO DO ; gerer le profil precedent

                # Pour chaque repas de reference, on cree une instance de repas
                # en copiant les parametres de la reference
                # on l'associe a la semaine en cours de creation
                for reference_repas in liste_reference_repas:
                    repas = models.Repas(nom=reference_repas.nom,
                                         ordre=reference_repas.ordre,
                                         actif=reference_repas.actif,
                                         libre_choix=reference_repas.libre_choix,
                                         invite=reference_repas.invite,
                                         semaine=semaine)
                    repas.save()
                    repas.saison = reference_repas.saison.all()
                    repas.categorie = reference_repas.categorie.all()
                    repas.save()
                return redirect('editer_profil_semaine')
            else:
                return render(request, 'menu/generer_nouvelle_semaine.html',
                              {"form_semaine": form})
    else:
        semaine = models.SemaineRempli()
        semaine.save()
        request.session['semaine_id'] = semaine.id
        form = forms.SemaineRempli(instance=semaine)
        return render(request, 'menu/generer_nouvelle_semaine.html', {"form_semaine": form})


def editer_profil_semaine(request):
    print('editer_profil_semaine')
    semaine_id = request.session.get('semaine_id')
    if semaine_id:
        semaine = models.SemaineRempli.objects.get(id=semaine_id)
    else:
        print('editer_profil_semaine : pas de semaine en sessions')

    repas_form_set = modelformset_factory(models.Repas, fields=('nom', 'actif', 'libre_choix', 'invite', 'saison',
                                                              'categorie'), extra=0)

    if request.method == 'POST':  # S'il s'agit d'une requête POST
        print("C'est un post'")
        # Nous reprenons les données
        formset = repas_form_set(request.POST, queryset=semaine.repas_set.all().order_by('ordre'))
        if formset.is_valid():  # Nous vérifions que les données sont valides
            print("Forme est valide")
            formset.save()
            return redirect('generer_menu')
        else:
            return render(request, 'menu/editer_profil_semaine.html', {'formset': formset})

    else:  # Si ce n'est pas du POST, c'est probablement une requête GET
        formset = repas_form_set(queryset=semaine.repas_set.all().order_by('ordre'))

    return render(request, 'menu/editer_profil_semaine.html', {'formset': formset})


def generer_menu(request):
    print('generer_menu')
    semaine_id = request.session.get('semaine_id')
    semaine = models.SemaineRempli.objects.get(id=semaine_id)
    # On cree un formset avec sur le model Repas
    repas_form_set = modelformset_factory(models.Repas, fields=('saison', 'categorie', 'recette'),
                                          widgets={'categorie': forms.forms.CheckboxSelectMultiple(),
                                                   'saison': forms.forms.CheckboxSelectMultiple()}, extra=0)

    if request.method == 'POST':
        # On modifie la semaine avec les donnees recuperees
        formset = repas_form_set(request.POST, queryset=semaine.repas_set.all().order_by('ordre'))

        if formset.is_valid():
            formset.save()
            return render(request, 'menu/generer_menu.html', {'repas_semaine': semaine})
        else:
            print("forme pas valide")
            print(formset.errors)
            return render(request, 'menu/generer_menu.html',  {'repas_semaine': semaine, 'formset': formset})
    else:
        # pour chaque repas de la semaine, trouver une recette
        repass = semaine.repas_set.all()
        for repas in repass:
            # on va ensuite trouver un recette associee
            recettes = trouver_recette(repas)
            if recettes:
                repas.recette = random.choice(recettes)
            else:
                print('pas de recette trouve')
                pass
            repas.save()

        # On le prerempli avec les repas de la semaine
        formset = repas_form_set(queryset=semaine.repas_set.all().order_by('ordre'))
        return render(request, 'menu/generer_menu.html', {'repas_semaine': semaine, 'formset': formset})


def menu_modifier(request, form_id):
    print('menu_modifier')
    semaine_id = request.session.get('semaine_id')
    semaine = models.SemaineRempli.objects.get(id=semaine_id)
    # On cree un formset avec sur le model Repas
    repas_form_set = modelformset_factory(models.Repas, fields=('saison', 'categorie', 'recette'),
                                          widgets={'categorie': forms.forms.CheckboxSelectMultiple(),
                                                   'saison': forms.forms.CheckboxSelectMultiple()}, extra=0)

    if request.method == 'POST':
        # On modifie la semaine avec les donnees recuperees
        formset = repas_form_set(request.POST, queryset=semaine.repas_set.all().order_by('ordre'))

        print("formset")
        print(dir(formset))
        #print(formset.queyset())
        print("formset.data")
        print(formset.get_queryset())

        if formset.is_valid():
            formset.save()
            # on recupere le repas a changer
            repas = semaine.repas_set.get(id=form_id)
            print(repas)
            recettes = trouver_recette(repas)
            print(recettes)
            # si le plat est trouve, on en choisit un au hasard
            if recettes:
                repas.recette = random.choice(recettes)
            else:
                repas.recette = None
            repas.save()
            formset = repas_form_set(queryset=semaine.repas_set.all().order_by('ordre'))
            return render(request, 'menu/generer_menu.html', {'repas_semaine': semaine, 'formset': formset})
        else:
            print("forme pas valide")
            print(formset.errors)
            return render(request, 'menu/generer_menu.html',  {'repas_semaine': semaine, 'formset': formset})
    else:
        print("On ne devrait pas etre ici")



def entrer_recette(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = forms.RecetteForm(request.POST)  # Nous reprenons les données
        if form.is_valid():  # Nous vérifions que les données sont valides
            form.save()
            return render(request, 'menu/accueil.html', locals())
        else:
            print("Forme n'est pas valide")

    else:  # Si ce n'est pas du POST, c'est probablement une requête GET
        form = forms.RecetteForm()  # Nous créons un formulaire vide

    return render(request, 'menu/entrer_recette.html', locals())


def accueil(request):
    return render(request, 'menu/accueil.html')


def verifier_semaine_duplique(request, numero_semaine):
    liste_semaine = models.SemaineRempli.objects.all()
    liste_numero_semaine = [semaine.numero_semaine for semaine in liste_semaine]
    print(numero_semaine)
    if numero_semaine in liste_numero_semaine:
        pass
        # add a warning


def liste_recette(request):
    liste_recette = models.Recette.objects.all()
    return render(request, 'menu/liste_recette.html', {'liste_recette':
                                                           liste_recette})


def voir_detail(request, id):
    recette = get_object_or_404(models.Recette, id=id)
    liste_saison = recette.saison.all()
    liste_categorie = recette.categorie.all()
    liste_ingredient = recette.ingredients.all()

    return render(request, 'menu/detail_recette.html', {'recette': recette,
                                                        'saisons': liste_saison, 'categories': liste_categorie,
                                                        'ingredients': liste_ingredient, "id": id})


def recette_aleatoire(request):
    recette = random.choice(models.Recette.objects.all())
    liste_saison = recette.saison.all()
    liste_categorie = recette.categorie.all()
    liste_ingredient = recette.ingredients.all()

    return render(request, 'menu/detail_recette.html', {'recette': recette,
                                                        'saisons': liste_saison, 'categories': liste_categorie,
                                                        'ingredients': liste_ingredient, "id": recette.id})


def voir_semaine(request, semaine_id):
    if semaine_id:
        request.session['semaine_id'] = semaine_id
        semaine = models.SemaineRempli.objects.get(id=semaine_id)
        return render(request, 'menu/generer_menu.html',
                      {'repas_semaine': semaine})
    else:
        return render(request, 'menu/generer_menu.html')


def reediter_menu_semaine(request):
    semaine_id = request.session.get('semaine_id')
    semaine = models.SemaineRempli.objects.get(id=semaine_id)
    form = forms.SemaineRempli(instance=semaine)
    return render(request, 'menu/generer_menu.html',
                  {'repas_semaine': semaine, 'form': form})


def trouver_recette(repas):
    query_object = Q()
    requete_trouve = False
    requete_vide = True

    # si le choix est libre on ne cheche pas de recette
    if repas.libre_choix:
        return None
    else:
        # on recupere le nom des saisons et des categories dans des
        # listes locales
        nom_saison = [saison.nom for saison in repas.saison.all()]
        nom_categorie = [categorie.nom for categorie
                         in repas.categorie.all()]
        if "Indifferent" in nom_saison:
            print("saison indifferent")
            if "Indifferent" in nom_categorie:
                print("et cat indifferente")
                requete_trouve = True
                # pas de critere donc la query est vide
            else:
                print("mais pas cat indifferente")
                requete_trouve = True
                requete_vide = False
                query_object = Q(categorie__in=repas.categorie.all()) | \
                               Q(categorie__nom="Indifferent")

        if not requete_trouve:
            if "Indifferent" in nom_categorie:
                print("cat indifferente")
                requete_trouve = True
                requete_vide = False
                query_object = Q(saison__in=repas.saison.all()) | \
                               Q(saison__nom="Indifferent")
            else:
                print("tout compte")
                requete_trouve = True
                requete_vide = False
                query_object = Q(categorie__in=repas.categorie.all()) | \
                               Q(categorie__nom="Indifferent")

                query_object.add(Q(saison__in=repas.saison.all()) |
                                 Q(saison__nom="Indifferent"), Q.AND)
        # enfin, on regarde s'il y a des invites
        if repas.invite:
            print("repas invite")
            requete_vide = False
            query_object.add(Q(OK_invites=True), Q.AND)

        # ici le query_object est pret, on fait donc la query a la base
        if not requete_vide:
            print("ici")
            print(query_object)
            recettes = models.Recette.objects.filter(query_object)
        else:
            print("la")
            recettes = models.Recette.objects.all()[::1]
    return recettes


def liste_semaines_precedentes(request):
    liste_semaine = models.SemaineRempli.objects.all(). \
        order_by('numero_semaine')

    return render(request, 'menu/voir_liste_semaine.html',
                  {'liste_semaine': liste_semaine})
