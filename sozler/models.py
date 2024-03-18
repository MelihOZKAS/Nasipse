from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from sairler.models import Sairler
from django.conf import settings
from siirler.models import SiirAltKategori




HELP_TEXTS = {
    "title": "Eğer Bir Ünlü ise sadece 'Sözleri' yazman yeterli.",
    "Model": "Modele göre sılanma ve konumlandırılma olacaktır.",
    "yazar": "Şiiri yazan kullanıcıyı seçin.",
    "slug": "Şiirin URL'de görünecek kısmını girin.",
    "kategorisi": "Şiirin kategorisini seçin.",
    "sair": "Şiirin şairini seçin.",
    "icerik": "Şiirin içeriğini girin.",
    "kapak_resmi": "Anasayfa Resim",
    "status": "Şiirin durumunu seçin.",
    "aktif": "Şiirin aktif olup olmadığını belirtin.",
    "meta_title": "Sayfanın meta başlığını girin.",
    "meta_description": "Sayfanın meta açıklamasını girin.",
    "keywords": "Sayfanın anahtar kelimelerini \" Virgül '  ' \" ile ayrınız. ",
    "banner": "Ana Sayfadaki büyük resim alanında ögrünür",
    "small_banner": "Ana sayfada küçük resimlerde görünür.",
    "hakkinda": "Şiir hakkında anlatılmak istenen.",
}
status_cho = (
    ("Taslak","Taslak"),
    ("Hazir","Hazir"),
    ("Yayinda","Yayinda"),
    ("Kontrol","Kontrol"),
    ("Reddedildi","Reddedildi"),
)

model_tipi = (
    ("Şiirler","Şiirler"),
    ("Şairler","Şairler"),
    ("Sözler","Sözler"),
    ("Hikayeler","Hikayeler"),
    ("EnglishSiir","EnglishSiir"),
)



class Sozler(models.Model):

    title = models.CharField(max_length=255,help_text=HELP_TEXTS["title"])
    yazar = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        help_text=HELP_TEXTS["yazar"])
    slug = models.SlugField(max_length=255,unique=True,blank=True,
        help_text=HELP_TEXTS["slug"])
    alt_kategorisi = models.ManyToManyField(SiirAltKategori, blank=True,
        help_text="Şiirin alt kategorilerini seçin.")
    sair = models.ForeignKey(Sairler,on_delete=models.SET_NULL, null=True,
        help_text=HELP_TEXTS["sair"])

    Model = models.CharField(max_length=20, choices=model_tipi,help_text=HELP_TEXTS["Model"])

    icerik = RichTextField(null=True,blank=True,
        help_text=HELP_TEXTS["icerik"])

    meta_description = models.TextField(
        blank=True,
        verbose_name="Meta Açıklama",
        help_text=HELP_TEXTS["meta_description"]
    )
    keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Anahtar Kelimeler",
        help_text=HELP_TEXTS["keywords"]
    )


    status = models.CharField(max_length=10, choices=status_cho, default="Taslak",
        help_text=HELP_TEXTS["status"])

    usermi = models.BooleanField(default=False)
    aktif = models.BooleanField(default=True,
        help_text=HELP_TEXTS["aktif"])
    banner = models.BooleanField(default=False,
        help_text=HELP_TEXTS["banner"])
    small_banner = models.BooleanField(default=False,
        help_text=HELP_TEXTS["small_banner"])
    aciklama = models.CharField(max_length=255, null=True, blank=True)
    okunma_sayisi = models.PositiveBigIntegerField(default=0)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    def okundu(self):
        self.okunma_sayisi += 1
        self.save(update_fields=['okunma_sayisi'])
        if self.sair:
            self.sair.okunma_sayisi += 1
            self.sair.save(update_fields=['okunma_sayisi'])

    def save(self, *args, **kwargs):
        if self.sair and not self.pk:
            self.title = f"{self.sair.title} - {self.title}"
            self.slug = f"{self.sair.slug}-{slugify(self.title.split(' - ')[-1])}"
        if not self.slug:
            self.slug = slugify(self.title)
        count = 1
        original_slug = self.slug
        original_title = self.title
        while Sozler.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{count}"
            self.title = f"{original_title} - {count}"
            count += 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Tüm Sözler"




class FavoriSozler(models.Model):
    soz = models.ForeignKey(Sozler, on_delete=models.CASCADE)
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)


class BegeniSozler(models.Model):
    soz = models.ForeignKey(Sozler, on_delete=models.CASCADE)
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)


class YorumSozler(models.Model):
    soz = models.ForeignKey(Sozler, on_delete=models.CASCADE, related_name='yorumlar')
    yazar = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    icerik = models.TextField()
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)