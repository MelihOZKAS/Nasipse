"""
URL configuration for Nasipsiir project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'sozler'
urlpatterns = [
    path("", views.yazar_home_detail, name="home"),
    path('tum-sozler-kategorileri/', views.all_Kategori, name='tum-soz-kategorileri'),
    path('populer-guzel-sozler/', views.TumSozlerSade, name='populer-guzel-sozler'),  # Coklu Sayfa

    path('begen/<int:soz_id>/', views.begen, name='begen'),  # Fav + Beğen özellikleri
    path('begen-kaldir/<int:soz_id>/', views.begen_kaldir, name='begen-kaldir'),  # Fav + Beğen özellikleri
    path('favori/<int:soz_id>/', views.favori, name='favori'),  # Fav + Beğen özellikleri
    path('favori-kaldir/<int:soz_id>/', views.favori_kaldir, name='favori-kaldir'),  # Fav + Beğen özellikleri

    # path('cok-okunan-siirler/', views.coklu_sayfa, name='cok-okunan-siirler'),#Coklu Sayfa
    path('en-son-eklenen-guzel-sozler/', views.TumSozlerSade, name='en-son-eklenen-guzel-sozler'),  # Coklu Sayfa
    path('<str:soz_slug>/', views.soz_detail, name='soz_slug'),
    path('guzel-sozler/<str:sair_slug>/', views.TumSozler, name='TumSozler'),
    path('kategori/<str:alt_kategori_slug>/', views.alt_kategori_detail, name='alt_kategori_detail'),
]
