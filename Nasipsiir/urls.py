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
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.sitemaps.views import index, sitemap
from .sitemaps import SiirAltKategoriSitemap, SiirlerSitemap,HikayeAltKategoriSitemap,HikayelerSitemap,SairlerSitemap,SozlerSitemap,SozlerAltKategoriSitemap,CustomUserSitemap
from django.views.generic.base import TemplateView

from django.views.static import serve
from django.conf import settings
from django.urls import re_path
from django.http import Http404
from django.shortcuts import render



sitemaps = {
    'siir_alt_kategoriler': SiirAltKategoriSitemap,
    'siirler': SiirlerSitemap,
    'hikaye_alt_kategoriler': HikayeAltKategoriSitemap,
    'hikayeler': HikayelerSitemap,
    'sairler': SairlerSitemap,
    'sozler': SozlerSitemap,
    'sozler_alt_kategori': SozlerAltKategoriSitemap,
    'diger-yazar': CustomUserSitemap,
}

def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response


urlpatterns = [
    path("yonetici/", admin.site.urls),
    path("", views.home, name="home"),
    path('404/', handler404, name='404'),
    path("siir/", include("siirler.urls")),
    path("sairler/", include("sairler.urls")),
    path("sozler/", include("sozler.urls")),
    path("kullanici/", include("userPanel.urls")),
    path("hikaye/", include("hikayeler.urls")),
    path("kayit-ol/",views.kayitol, name="kayit-ol"),
    path("giris-yap/",views.girisyap, name="giris-yap"),
    path("sms-kontrol/",views.SMSKontrol, name="sms-kontrol"),
    path("cikis-yap/",views.cikis, name="cikis-yap"),
    #re_path(r'^robots\.txt$', serve, {'path': 'robots.txt', 'document_root': settings.BASE_DIR}),
    path("robots.txt",views.robots_txt, name="robots"),
    path('sitemap.xml', index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)