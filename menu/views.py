import random
from datetime import timedelta, date

from django.db.models import Q
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from . import forms
from . import models
from . import generatePdf


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

    return render(request, 'menu/editer_recette.html', {'form': form, 'id': recette.id})


def generer_semaine(request):
    """This method handles the very beginning of the week menu creation

    It allows to chose
    - the week number
    - the week profile
    Once done each daily profile is created and saved.
    The user is then routed to the actual menu creation
    """
    # if the user submitted the form
    if request.method == 'POST':
        # if the user actually wanted to continue.
        if 'submit' in request.POST:
            print("submit generer_semaine")
            semaine = models.SemaineRempli()
            # On modifie la semaine avec les donnees recuperees
            form = forms.SemaineRempli(request.POST, instance=semaine)
            if form.is_valid():
                week_number = form.cleaned_data['numero_semaine']
                print(week_number)
                if is_week_duplicated(week_number):
                    return render(request, 'menu/generer_nouvelle_semaine.html', {"form_semaine": form, "warning":
                        "La semaine existe deja"})
                # if all is fine, the week is saved.
                form.save()

                # we store the week id in the live session.
                request.session['semaine_id'] = semaine.id
                # we get the profile (=the season) from the week
                reference_saison = models.ReferenceSaison.objects.filter(nom=form.cleaned_data['profil'])
                # we get the list of meals from the reference.
                reference_repass = models.ReferenceRepas.objects.filter(profil=reference_saison)
                # TO DO ; gerer le profil precedent
                # for each reference meal, we create a meal instance that is associated to the current week
                # the meal parameters are copies from the reference meal
                for reference_repas in reference_repass:
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
                return render(request, 'menu/generer_nouvelle_semaine.html', {"form_semaine": form})
        else:
            # The user wants to abort the week menu creation
            print("Abort week creation")
            return render(request, 'menu/accueil.html')

    else:
        # It means it is the first time the user accesses the template
        # We create the model. The week number is populated automatically in the model
        semaine = models.SemaineRempli()
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
    week_id = request.session.get('semaine_id')
    week = models.SemaineRempli.objects.get(id=week_id)
    # A formset is created from the model Repas and the form RepasFormLeger
    repas_form_set = modelformset_factory(models.Repas, form=forms.RepasFormLeger, extra=0)

    if request.method == 'POST':
        # On modifie la semaine avec les donnees recuperees
        formset = repas_form_set(request.POST, queryset=week.repas_set.all().order_by('ordre'))

        if formset.is_valid():
            formset.save()
            # If the user validated the form, using the "Valider" button
            if 'validate' in request.POST:
                ingredients = list_ingredients(week.repas_set.all()[::1])
                update_week_ingredients(week.repas_set.all()[::1], week)
                return render(request, 'menu/generer_menu.html', {'repas_semaine': week, 'ingredients': ingredients})
            # Else the user requested a refresh
            else:
                return render(request, 'menu/generer_menu.html', {'repas_semaine': week, 'formset': formset})
        else:
            print("forme pas valide")
            print(formset.errors)
            return render(request, 'menu/generer_menu.html',  {'repas_semaine': week, 'formset': formset})
    else:
        # pour chaque repas de la semaine, trouver une recette
        repass = week.repas_set.all()
        for repas in repass:
            # on va ensuite trouver un recette associee
            recettes = trouver_recette_de_repas(repas)
            if recettes:
                repas.recette = random.choice(recettes)
                print("Repas id = {}".format(repas.id))
            else:
                print('pas de recette trouve')
                pass
            repas.save()

        # On le prerempli avec les repas de la semaine
        formset = repas_form_set(queryset=week.repas_set.all().order_by('ordre'))
        return render(request, 'menu/generer_menu.html', {'repas_semaine': week, 'formset': formset})


def send(request):
    print("send")
    week_id = request.session.get('semaine_id')
    week = models.SemaineRempli.objects.get(id=week_id)

    fish_items = week.purchase_items.filter(type__name="Fish")[::1] + week.\
        ingredients.filter(type__name="Fish")[::1]
    print("fish_items")
    print(fish_items)
    vegetable_shop_items = week.purchase_items.filter(type__name="Vegetable_shop")[::1] + week.\
        ingredients.filter(type__name="Vegetable_shop")[::1]
    print("vegetable_shop_items")
    print(vegetable_shop_items)
    milky_items = week.purchase_items.filter(type__name="Milky")[::1] + week.ingredients.\
        filter(type__name="Milky")[::1]
    print("milky_items")
    print(milky_items)
    meats_items = week.purchase_items.filter(type__name="Meats")[::1] + week.ingredients.\
        filter(type__name="Meats")[::1]
    print("meats_items")
    print(meats_items)
    fruit_vegetable_items = week.purchase_items.filter(type__name="Fruit_vegetable")[::1] + week.ingredients.\
        filter(type__name="Fruit_vegetable")[::1]
    print("fruit_vegetable_items")
    print(fruit_vegetable_items)
    medecine_items = week.purchase_items.filter(type__name="Medecine")[::1] + week.\
        ingredients.filter(type__name="Medecine")[::1]
    print("medecine_items")
    print(medecine_items)
    organic_items = week.purchase_items.filter(type__name="Organic")[::1] + week.\
        ingredients.filter(type__name="Organic")[::1]
    print("organic_items")
    print(organic_items)
    salty_items = week.purchase_items.filter(type__name="Salty")[::1] + week.\
        ingredients.filter(type__name="Salty")[::1]
    print("salty_items")
    print(salty_items)
    sweet_items = week.purchase_items.filter(type__name="Sweet")[::1] + week.\
        ingredients.filter(type__name="Sweet")[::1]
    print("sweet_items")
    print(sweet_items)
    drink_items = week.purchase_items.filter(type__name="Drink")[::1] + week.\
        ingredients.filter(type__name="Drink")[::1]
    print("drink_items")
    print(drink_items)
    home_items = week.purchase_items.filter(type__name="Home")[::1] + week.\
        ingredients.filter(type__name="Home")[::1]
    print("home_items")
    print(home_items)
    frozen_items = week.purchase_items.filter(type__name="Frozen")[::1] + week.\
        ingredients.filter(type__name="Frozen")[::1]
    print("frozen_items")
    print(frozen_items)
    no_type_items = week.purchase_items.filter(type__name__isnull=True, type__isnull=True)[::1] + week.\
        ingredients.filter(type__name__isnull=True, type__isnull=True)[::1]
    print("no_type_items")
    print(no_type_items)

    ctxt = {"repas_semaine": week,
            'fish_items': fish_items,
            'vegetable_shop_items': vegetable_shop_items,
            'milky_items': milky_items,
            'meats_items': meats_items,
            'fruit_vegetable_items': fruit_vegetable_items,
            'medecine_items': medecine_items,
            'organic_items': organic_items,
            'salty_items': salty_items,
            'sweet_items': sweet_items,
            'drink_items': drink_items,
            'home_items': home_items,
            'frozen_items': frozen_items,
            'no_type_items': no_type_items,
            }

    s = generatePdf.GeneratePDF(template="menu/liste.html")
    s._make_pdf(ctxt=ctxt)

    email_ctx = {"week_nb": week.numero_semaine}
    subject="Liste des courses semaine {}".format(week.numero_semaine)
    s.send_pdf(subject=subject, email_template="menu/mail.html", ctxt=email_ctx)


def list_ingredients(repass):
    """This method extracts the list of names of necessary ingredients from the list of menus given as input
    It returns the extracted list"""
    print("lister_ingredients")
    necessary_ingredients = []
    for repas in repass:
        # recette can be empty (no menu found or inactive day)
        if repas.recette:
            # get all the ingredients of the menu
            ingredients = repas.recette.ingredients.all()
            # Update the list of necessary ingredients for each ingredient
            for ingredient in ingredients:
                update_necessary_ingredients(ingredient, necessary_ingredients, repas.recette.nom)

        print("necessary_ingredients")
        print(necessary_ingredients)
    return necessary_ingredients


def update_week_ingredients(repass, week):
    """This method extracts the list of names of necessary ingredients from the list of menus given as input
    and updates the filled week with them """
    print("update_week_ingredients")
    week.ingredients.clear()
    for repas in repass:
        # recette can be empty (no menu found or inactive day)
        if repas.recette:
            # get all the ingredients of the menu
            ingredients = repas.recette.ingredients.all()
            # Update the list of ingredients for the week
            for ingredient in ingredients:
                week.ingredients.add(ingredient)


def update_necessary_ingredients(ingredient, necessary_ingredients, recipe_name):
    """This method searches the ingredient in the list of necessary_ingredients
    if found it updates the number of recipe for which the ingredient is necessary
    and add the recipe name to the list
    if not found, it creates a new ingredient and add it to the list
    """
    print('update_necessary_ingredients')
    new_ingredient = True
    # go through the list of already identified necessary ingredients
    for necessary_ingredient in necessary_ingredients:
        if necessary_ingredient.name == ingredient.nom:
            # if the current one is already identified, update the number of occurrence
            # and add the recipe name to the list
            necessary_ingredient.occurrence +=1
            necessary_ingredient.recipe_names.append(recipe_name)
            new_ingredient = False
    if new_ingredient:
        # if the current ingredient is not listed yet
        # create a new ingredient, and add it to the list
        new_necessary_ingredient = models.NecessaryIngredient(ingredient.nom, recipe_name)
        necessary_ingredients.append(new_necessary_ingredient)


def reediter_menu_semaine(request):
    print('reediter_menu_semaine')
    semaine_id = request.session.get('semaine_id')
    semaine = models.SemaineRempli.objects.get(id=semaine_id)
    # A formset is create from the model Repas and the form RepasFormLeger
    repas_form_set = modelformset_factory(models.Repas, form=forms.RepasFormLeger, extra=0)

    formset = repas_form_set(queryset=semaine.repas_set.all().order_by('ordre'))
    return render(request, 'menu/generer_menu.html', {'repas_semaine': semaine, 'formset': formset})


def menu_modifier(request, form_id):
    print('menu_modifier')
    semaine_id = request.session.get('semaine_id')
    semaine = models.SemaineRempli.objects.get(id=semaine_id)
    # A formset is create from the model Repas and the form RepasFormLeger
    repas_form_set = modelformset_factory(models.Repas, form=forms.RepasFormLeger, extra=0)

    if request.method == 'POST':
        # On modifie la semaine avec les donnees recuperees
        formset = repas_form_set(request.POST, queryset=semaine.repas_set.all().order_by('ordre'))

        if formset.is_valid():
            formset.save()
            print("formset.get_queryset() after save")
            print(formset.get_queryset())
            # on recupere le repas a changer
            repas = semaine.repas_set.get(id=form_id)

            # we get an associated list of matching receipts
            recettes = trouver_recette_de_repas(repas)
            # if receipts are found we chose one
            if recettes:
                repas.recette = random.choice(recettes)
            else:
                repas.recette = None
            repas.save()
            formset = repas_form_set(queryset=semaine.repas_set.all().order_by('ordre'))
            return render(request, 'menu/generer_menu.html', {'repas_semaine': semaine, 'formset': formset})
        else:
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


def is_week_duplicated(week_number):
    """This method checks that the week being created does not already exist in database
    It returns True in case of duplicate, False otherwise
    It selects the menu created six months before and after the current date.
    From this selection extracts all the week numbers
    And finally checks that the current week being created is not included in this list

    """

    # Get the current date minus and plus 6 months
    today_minus_six_months = date.today() - timedelta(weeks=30)
    today_plus_six_months = date.today() + timedelta(weeks=30)
    # Select all the created weeks in the interval
    weeks = models.SemaineRempli.objects.filter(date__gt=today_minus_six_months, date__lt=today_plus_six_months)
    # We extract the list of week numbers from the week list
    week_numbers = [week.numero_semaine for week in weeks]
    if week_number in week_numbers:
        print("There is a duplication")
        return True
    else:
        return False


def liste_recette(request):
    recettes = []
    if request.method == 'POST':
        form = forms.SelectionRecetteForm(request.POST)
        if form.is_valid():
            recettes = selectionner_recette(form)
            print("recettes", recettes)
        else:
            print("form for liste_recette is not valid")
    else:
        form = forms.SelectionRecetteForm()

    return render(request, 'menu/liste_recette.html', {'recettes': recettes, 'selection_form': form})


def selectionner_recette(selection_form):
    query_object = Q()
    requete_trouve = False
    requete_vide = True

    # on recupere le nom des saisons et des categories dans des
    # listes locales
    categories = [categorie.nom for categorie in selection_form.cleaned_data['categories']]
    saisons = [saison.nom for saison in selection_form.cleaned_data['saisons']]
    ingredients = [ingredient.nom for ingredient in selection_form.cleaned_data['ingredients']]
    invite_present = selection_form.cleaned_data['invite_present']

    print("categorie: ", categories)
    print("saisons: ", saisons)
    print("ingredients: ", ingredients)
    print("invite: ", invite_present)

    if not saisons or "Indifférent" in saisons:
        print("saison indifferente")
        if not categories or "Indifférent" in categories:
            print("et cat indifferente")
            requete_trouve = True
            # pas de critere donc la query est vide
        else:
            print("mais pas cat indifferente")
            requete_trouve = True
            requete_vide = False
            query_object = Q(categorie__in=selection_form.cleaned_data['categories']) | Q(categorie__nom="Indifférent")

    if not requete_trouve:
        if not categories or "Indifférent" in categories:
            print("cat indifferente")
            requete_trouve = True
            requete_vide = False
            query_object = Q(saison__in=selection_form.cleaned_data['saisons']) | Q(saison__nom="Indifférent")
        else:
            print("tout compte")
            requete_trouve = True
            requete_vide = False
            query_object = Q(categorie__in=selection_form.cleaned_data['categories']) | Q(categorie__nom="Indifférent")
            query_object.add(Q(saison__in=selection_form.cleaned_data['saisons']) | Q(saison__nom="Indifférent"), Q.AND)
    # On regarde ensuite s'il y a des invites
    if invite_present:
        requete_vide = False
        query_object.add(Q(OK_invites=True), Q.AND)

    # On regarde enfin si des ingredients sont specifies
    if ingredients:
        requete_vide = False
        query_object.add(Q(ingredients__in=selection_form.cleaned_data['ingredients']), Q.AND)

    # ici le query_object est pret, on fait donc la query a la base
    if not requete_vide:
        recettes = models.Recette.objects.filter(query_object).order_by('nom')
    else:
        recettes = models.Recette.objects.all().order_by('nom')[::1]
    return recettes


def voir_detail(request, id):
    recette = get_object_or_404(models.Recette, id=id)
    liste_saison = recette.saison.all()
    liste_categorie = recette.categorie.all()
    liste_ingredient = sorted(recette.ingredients.all(), key=lambda ingredient: ingredient.nom)

    return render(request, 'menu/detail_recette.html', {'recette': recette,
                                                        'saisons': liste_saison, 'categories': liste_categorie,
                                                        'ingredients': liste_ingredient, "id": id})


def recette_aleatoire(request):
    recette = random.choice(models.Recette.objects.all())
    liste_saison = recette.saison.all()
    liste_categorie = recette.categorie.all()
    liste_ingredient = sorted(recette.ingredients.all(), key=lambda ingredient: ingredient.nom)

    return render(request, 'menu/detail_recette.html', {'recette': recette,
                                                        'saisons': liste_saison, 'categories': liste_categorie,
                                                        'ingredients': liste_ingredient, "id": recette.id})


def voir_semaine(request, semaine_id):
    if semaine_id:
        request.session['semaine_id'] = semaine_id
        semaine = models.SemaineRempli.objects.get(id=semaine_id)
        ingredients = list_ingredients(semaine.repas_set.all()[::1])
        return render(request, 'menu/generer_menu.html', {'repas_semaine': semaine, 'ingredients': ingredients})
#        return render(request, 'menu/generer_menu.html', {'repas_semaine': semaine})
    else:
        return render(request, 'menu/generer_menu.html')


def trouver_recette_de_repas(repas):
    query_object = Q()
    requete_trouve = False
    requete_vide = True

    # si le choix est libre on ne cheche pas de recette
    if repas.libre_choix or not repas.actif:
        return None
    else:
        # on recupere le nom des saisons et des categories dans des listes locales
        saisons = [saison.nom for saison in repas.saison.all()]
        categories = [categorie.nom for categorie in repas.categorie.all()]

        if "Indifférent" in saisons:
            print("saison indifferent")
            if "Indifférent" in categories:
                print("et cat indifferente")
                requete_trouve = True
                # pas de critere donc la query est vide
            else:
                print("mais pas cat indifferente")
                requete_trouve = True
                requete_vide = False
                query_object = Q(categorie__in=repas.categorie.all()) | \
                               Q(categorie__nom="Indifférent")

        if not requete_trouve:
            if "Indifférent" in categories:
                print("cat indifferente")
                requete_trouve = True
                requete_vide = False
                query_object = Q(saison__in=repas.saison.all()) | \
                               Q(saison__nom="Indifférent")
            else:
                print("tout compte")
                requete_trouve = True
                requete_vide = False
                query_object = Q(categorie__in=repas.categorie.all()) | \
                               Q(categorie__nom="Indifférent")

                query_object.add(Q(saison__in=repas.saison.all()) |
                                 Q(saison__nom="Indifférent"), Q.AND)
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


def purchase_list(request):
        week_id = request.session['semaine_id']
        week = models.SemaineRempli.objects.get(id=week_id)
        ingredients = list_ingredients(week.repas_set.all()[::1])
        purchase_items = models.PurchaseItem.objects.all()

        for purchase_item in purchase_items:
            if purchase_item.recurring:
                week.purchase_items.add(purchase_item)

        week_form = forms.FilledWeekFormForPurchase(instance=week)

        if request.method == 'POST':
            week_form = forms.FilledWeekFormForPurchase(request.POST, instance=week)
            if week_form.is_valid():
                week_form.save()
                send(request)
                return render(request, 'menu/end.html')
            else:
                print("form for liste_recette is not valid")

        return render(request, 'menu/purchase_list.html', {'ingredients': ingredients,
                                                           'purchase_items': purchase_items,
                                                           'filled_week': week_form})

