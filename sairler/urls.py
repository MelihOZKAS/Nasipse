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

app_name = 'sairler'
urlpatterns = [
    path("", views.sair_home_detail, name="home"),
    path('begen/<int:siir_id>/', views.begen, name='begen'),  # Coklu Sayfa
    path('begen-kaldir/<int:siir_id>/', views.begen_kaldir, name='begen-kaldir'),  # Coklu Sayfa
    path('favori/<int:siir_id>/', views.favori, name='favori'),  # Coklu Sayfa
    path('favori-kaldir/<int:siir_id>/', views.favori_kaldir, name='favori-kaldir'),  # Coklu Sayfa
    path('populer-sairler/', views.populer_sair_detail, name='populer-sairler'),  # Coklu Sayfa
    path('<str:sair_slug>/', views.sair_detail, name='sair_detail'),
    #  path('kategori/<str:alt_kategori_slug>/', views.alt_kategori_detail, name='alt_kategori_detail'),
]

#path("", views.siir_home_detail, name="home"),
#path('tum-siir-kategorileri/', views.all_Kategori, name='tum-siir-kategorileri'),
#path('populer-siirler/', views.coklu_sayfa, name='populer-siirler'),  # Coklu Sayfa
#path('cok-okunan-siirler/', views.coklu_sayfa, name='cok-okunan-siirler'),  # Coklu Sayfa
#path('en-son-eklenen-siirler/', views.coklu_sayfa, name='en-son-eklenen-siirler'),  # Coklu Sayfa
#path('<str:siir_slug>/', views.siir_detail, name='siir_detail'),
#path('sair-eserleri/<str:sair_slug>/', views.sairTumeserleri, name='sair-eserleri'),
#path('kategori/<str:alt_kategori_slug>/', views.alt_kategori_detail, name='alt_kategori_detail'),
#