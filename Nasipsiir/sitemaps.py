from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from siirler.models import SiirAltKategori, Siirler
from hikayeler.models import HikayeAltKategori, Hikayeler
from sozler.models import Sozler
from sairler.models import Sairler
from userPanel.models import CustomUser


class SiirAltKategoriSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.3

    def items(self):
        return SiirAltKategori.objects.all()

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('siir:alt_kategori_detail', args=[obj.slug])


class SiirlerSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Siirler.objects.filter(aktif=True)

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('siir:siir_detail', args=[obj.slug])


class HikayeAltKategoriSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.3

    def items(self):
        return HikayeAltKategori.objects.all()


    def location(self, obj):
        return reverse('hikaye:alt_kategori_detail', args=[obj.slug])


class HikayelerSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Hikayeler.objects.all()
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye:hikaye_slug', args=[obj.slug])


class SairlerSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Sairler.objects.all()

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('sairler:sair_detail', args=[obj.slug])


class SozlerSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Sozler.objects.all()
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('sozler:soz_slug', args=[obj.slug])


class CustomUserSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return CustomUser.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('konsol:blog-yazar-detay', args=[obj.slug])