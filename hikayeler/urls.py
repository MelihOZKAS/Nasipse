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

app_name = 'hikaye'
urlpatterns = [
    path("", views.hikaye_home, name="home"),
    path('begen/<int:siir_id>/', views.begen, name='begen'),  # Coklu Sayfa
    path('begen-kaldir/<int:siir_id>/', views.begen_kaldir, name='begen-kaldir'),  # Coklu Sayfa
    path('favori/<int:siir_id>/', views.favori, name='favori'),  # Coklu Sayfa
    path('favori-kaldir/<int:siir_id>/', views.favori_kaldir, name='favori-kaldir'),  # Coklu Sayfa

    path('tum-hikaye-kategorileri/', views.all_Kategori, name='tum-hikaye-kategorileri'),

    path('populer-hikayeler/', views.coklu_sayfa, name='populer-hikayeler'),#Coklu Sayfa
    path('cok-okunan-hikayeler/', views.coklu_sayfa, name='cok-okunan-hikaye'),#Coklu Sayfa
    path('cok-begeni-alan-hikayeler/', views.coklu_sayfa, name='cok-begeni-alan-hikayeler'),#Coklu Sayfa
    path('en-son-eklenen-hikayeler/', views.coklu_sayfa, name='en-son-eklenen-hikaye'),#Coklu Sayfa


    path('<str:hikaye_slug>/', views.hikaye_detail, name='hikaye_slug'),
    # path('guzel-sozler/<str:sair_slug>/', views.TumSozler, name='TumSozler'),
    path('kategori/<str:alt_kategori_slug>/', views.alt_kategori_detail, name='alt_kategori_detail'),
]
