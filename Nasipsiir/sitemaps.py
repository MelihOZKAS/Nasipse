from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from siirler.models import SiirAltKategori, Siirler

class SiirAltKategoriSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return SiirAltKategori.objects.all()

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('alt_kategori_detail', args=[obj.slug])

class SiirlerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Siirler.objects.filter(aktif=True)

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('siir_detail', args=[obj.slug])
