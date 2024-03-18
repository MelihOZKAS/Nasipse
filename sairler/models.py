from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.conf import settings

from Nasipsiir.custom_storages import ImageSettingStorage


def kapak_resmi_upload_to(instance, filename):
    # Dosya adını değiştir
    yeni_ad = f"{instance.slug}"
    # Dosya uzantısını koru
    uzanti = filename.split('.')[-1]
    # Yeni dosya adını döndür
    return f"kapak_resimleri/{yeni_ad}.{uzanti}"


HELP_TEXTS = {
    "title": "Şiirin başlığını girin.",
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
    "SairOzet": "Şiirlerin altında görüncek yazı.",
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


# Create your models here.
class Sairler(models.Model):
    title = models.CharField(max_length=255, help_text=HELP_TEXTS["title"])
    yazar = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                              help_text=HELP_TEXTS["yazar"])
    slug = models.SlugField(max_length=255, unique=True, blank=True,
                            help_text=HELP_TEXTS["slug"])

    Model = models.CharField(max_length=20, choices=model_tipi, help_text=HELP_TEXTS["Model"])

    icerik = RichTextField(null=True, blank=True,
                           help_text=HELP_TEXTS["icerik"])

    SairOzet = RichTextField(null=True, blank=True,
                             help_text=HELP_TEXTS["SairOzet"])

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

    #kapak_resmi = models.ImageField(upload_to=kapak_resmi_upload_to,help_text=HELP_TEXTS["kapak_resmi"])
    kapak_resmi = models.ImageField(upload_to=kapak_resmi_upload_to,
                                    storage=ImageSettingStorage(),
                                    help_text=HELP_TEXTS["kapak_resmi"], null=True, blank=True)

    status = models.CharField(max_length=10, choices=status_cho, default="Taslak",
                              help_text=HELP_TEXTS["status"])
    usermi = models.BooleanField(default=False)
    aktif = models.BooleanField(default=True,
                                help_text=HELP_TEXTS["aktif"])
    banner = models.BooleanField(default=False,
                                 help_text=HELP_TEXTS["banner"])
    small_banner = models.BooleanField(default=False,
                                       help_text=HELP_TEXTS["small_banner"])
    okunma_sayisi = models.PositiveBigIntegerField(default=0)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    def okundu(self):
        self.okunma_sayisi += 1
        self.save(update_fields=['okunma_sayisi'])




    class Meta:
        verbose_name_plural = "Tüm Şairler"

    def __str__(self):
        return self.title



class FavoriSair(models.Model):
    sair = models.ForeignKey(Sairler, on_delete=models.CASCADE)
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

class BegeniSair(models.Model):
    sair = models.ForeignKey(Sairler, on_delete=models.CASCADE)
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

class YorumSair(models.Model):
    sair = models.ForeignKey(Sairler, on_delete=models.CASCADE, related_name='yorumlar')
    yazar = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    icerik = models.TextField()
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
