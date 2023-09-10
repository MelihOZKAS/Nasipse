from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

from Nasipsiir.custom_storages import ImageSettingStorage


#from django.utils.text import slugify

# Create your models here.

def kapak_resmi_upload_to(instance, filename):
    # Dosya adını değiştir
    yeni_ad = f"{instance.slug}"
    # Dosya uzantısını koru
    uzanti = filename.split('.')[-1]
    # Yeni dosya adını döndür
    return f"kapak_resimleri/{yeni_ad}.{uzanti}"


HELP_TEXTS = {
    "title": "Hikayenin başlığını girin.",
    "Model": "Modele göre sılanma ve konumlandırılma olacaktır.",
    "yazar": "Hikayeyi yazan kullanıcıyı seçin.",
    "slug": "Hikayeyi URL'de görünecek kısmını girin.",
    "kategorisi": "Hikayeyi kategorisini seçin.",
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
    "Acikalama": "Kullanıcının işlem durumunu gösterir.",
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




class HikayeAltKategori(models.Model):
    alt_kategori_adi = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    #kapak_resmi = models.ImageField(upload_to=kapak_resmi_upload_to,help_text=HELP_TEXTS["kapak_resmi"])
    kapak_resmi = models.ImageField(upload_to=kapak_resmi_upload_to,
                                    storage=ImageSettingStorage(),
                                    help_text=HELP_TEXTS["kapak_resmi"], null=True, blank=True)
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

    aktif = models.BooleanField(default=True)
    banner = models.BooleanField(default=False)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Tüm Alt Kategoriler"

    def __str__(self):
        return self.alt_kategori_adi



class Hikayeler(models.Model):
    title = models.CharField(max_length=255,help_text=HELP_TEXTS["title"])
    yazar = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        help_text=HELP_TEXTS["yazar"])
    slug = models.SlugField(max_length=255,unique=True,blank=True,
        help_text=HELP_TEXTS["slug"])

    Model = models.CharField(max_length=20, choices=model_tipi,help_text=HELP_TEXTS["Model"])
    alt_kategorisi = models.ManyToManyField(HikayeAltKategori, blank=True,
                                            help_text="Şiirin alt kategorilerini seçin.")

    icerik = RichTextField(null=True,blank=True,
        help_text=HELP_TEXTS["icerik"])

    hakkinda = RichTextField(null=True,blank=True,
        help_text=HELP_TEXTS["hakkinda"])

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
    status = models.CharField(max_length=10, choices=status_cho, default="Taslak",
        help_text=HELP_TEXTS["status"])
    usermi = models.BooleanField(default=False)
    aktif = models.BooleanField(default=True,
        help_text=HELP_TEXTS["aktif"])
    banner = models.BooleanField(default=False,
        help_text=HELP_TEXTS["banner"])
    small_banner = models.BooleanField(default=False,
        help_text=HELP_TEXTS["small_banner"])
    aciklama = models.CharField(max_length=255,null=True,blank=True, help_text=HELP_TEXTS["Acikalama"])
    okunma_sayisi = models.PositiveBigIntegerField(default=0)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    def okundu(self):
        self.okunma_sayisi += 1
        self.save()
    class Meta:
        verbose_name_plural = "Tüm Hikayeler"





class FavoriHikayeler(models.Model):
    hikayeler = models.ForeignKey(Hikayeler, on_delete=models.CASCADE)
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)


class BegeniHikayeler(models.Model):
    hikayeler = models.ForeignKey(Hikayeler, on_delete=models.CASCADE)
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)


class YorumHikayeler(models.Model):
    hikayeler = models.ForeignKey(Hikayeler, on_delete=models.CASCADE, related_name='yorumlar')
    yazar = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    icerik = models.TextField()
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
