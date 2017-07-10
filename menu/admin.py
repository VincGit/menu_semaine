from django.contrib import admin
from menu.models import Categorie, Saison, Recette, Repas, Ingredient, \
ReferenceRepas, SemaineRempli, ReferenceSaison


class RecetteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'OK_invites', 'date')
    list_filter = ('nom', 'OK_invites', 'date')
    ordering = ('nom', )
    search_fields = ('nom', 'categorie', 'saison', 'OK_invites')


class IngredientAdmin(admin.ModelAdmin):
    ordering = ('nom',)


class SemaineRempliAdmin(admin.ModelAdmin):
    list_display = ('numero_semaine', 'profil', 'date')
    ordering = ('date', )


admin.site.register(Categorie)
admin.site.register(Saison)
admin.site.register(Recette, RecetteAdmin)
admin.site.register(Repas)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(ReferenceRepas)
admin.site.register(ReferenceSaison)
admin.site.register(SemaineRempli, SemaineRempliAdmin)