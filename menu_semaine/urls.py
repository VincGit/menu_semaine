from django.conf.urls import include, url
from django.contrib import admin
from menu import views

urlpatterns = [
    url(r'^$', views.accueil, name='accueil'),
    url(r'^menu/', include('menu.urls')),
#    url(r'^admin/', include(admin.site.urls)),
]
