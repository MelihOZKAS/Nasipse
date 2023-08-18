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

app_name = 'konsol'
urlpatterns = [
    path("", views.konsol_home_detail, name="home"),
    path('siir-detay-listesi/', views.SiirDetayListesi, name='siir-detay-listesi'),  # Coklu Sayfa
    path('soz-detay-listesi/', views.SozDetayListesi, name='soz-detay-listesi'),
    path('hikaye-detay-listesi/', views.HikayeDetayListesi, name='hikaye-detay-listesi'),

    path('siir-ekle/', views.SiirEkle, name='siir-ekle'), #Paylas OK
    path('soz-ekle/', views.SozEkle, name='soz-ekle'), #Paylas OK
    path('hikaye-ekle/', views.SozEkle, name='hikaye-ekle'), #Paylas OK

    path('begen/<int:yazar_id>/', views.begen, name='begen'),  # Fav + Beğen özellikleri
    path('begen-kaldir/<int:yazar_id>/', views.begen_kaldir, name='begen-kaldir'),  # Fav + Beğen özellikleri
    path('favori/<int:yazar_id>/', views.favori, name='favori'),  # Fav + Beğen özellikleri
    path('favori-kaldir/<int:yazar_id>/', views.favori_kaldir, name='favori-kaldir'),  # Fav + Beğen özellikleri



    path('favori-sairler/', views.TumFavoriler, name='favori-sair'), #OK
    path('favori-siirler/', views.TumFavoriler, name='favori-siirler'), #OK
    path('favori-sozler/', views.TumFavoriler, name='favori-sozler'), #OK
    path('favori-hikayeler/', views.TumFavoriler, name='favori-hikayeler'), #OK
    path('favori-kullanici/', views.TumFavoriler, name='favori-kullanici'), #OK

    path('begeni-sairler/', views.TumBegeni, name='begeni-sairler'),  # OK
    path('begeni-siirler/', views.TumBegeni, name='begeni-siirler'),  # OK
    path('begeni-sozler/', views.TumBegeni, name='begeni-sozler'),  # OK
    path('begeni-hikayeler/', views.TumBegeni, name='begeni-hikayeler'),  # OK
    path('begeni-kullanici/', views.TumBegeni, name='begeni-kullanici'),  # OK

    path('begenilen-siirler/', views.SiirDetayListesi, name='begenilen-siirler'),
    path('yazar-hakkinda/<str:yazar>/', views.yazar_detail, name='blog-yazar-detay'),
    path('yazar-eserleri/<str:yazar>/', views.yazar_tum_eserleri, name='blog-yazar-eserleri'),
]