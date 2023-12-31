# Generated by Django 4.2.3 on 2023-08-02 23:34

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import siirler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sairler", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AnasayfaKeyler",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Şiirin başlığını girin.", max_length=255
                    ),
                ),
                (
                    "meta_title",
                    models.CharField(
                        blank=True,
                        help_text="Sayfanın meta başlığını girin.",
                        max_length=255,
                        verbose_name="Meta Başlık",
                    ),
                ),
                (
                    "meta_description",
                    models.TextField(
                        blank=True,
                        help_text="Sayfanın meta açıklamasını girin.",
                        verbose_name="Meta Açıklama",
                    ),
                ),
                (
                    "keywords",
                    models.CharField(
                        blank=True,
                        help_text="Sayfanın anahtar kelimelerini \" Virgül '  ' \" ile ayrınız. ",
                        max_length=255,
                        verbose_name="Anahtar Kelimeler",
                    ),
                ),
                (
                    "kapak_resmi",
                    models.ImageField(
                        blank=True,
                        help_text="Anasayfa Resim",
                        null=True,
                        upload_to="AnaSayfaResmi",
                    ),
                ),
            ],
            options={"verbose_name_plural": "AnaSayfaSeo Ayarları",},
        ),
        migrations.CreateModel(
            name="SiirAltKategori",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("alt_kategori_adi", models.CharField(max_length=30, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True)),
                ("sozler_title", models.CharField(blank=True, max_length=255)),
                ("sozler_slug", models.SlugField(blank=True, max_length=255)),
                (
                    "kapak_resmi",
                    models.ImageField(
                        help_text="Anasayfa Resim",
                        upload_to=siirler.models.kapak_resmi_upload_to,
                    ),
                ),
                (
                    "meta_description",
                    models.TextField(
                        blank=True,
                        help_text="Sayfanın meta açıklamasını girin.",
                        verbose_name="Meta Açıklama",
                    ),
                ),
                (
                    "keywords",
                    models.CharField(
                        blank=True,
                        help_text="Sayfanın anahtar kelimelerini \" Virgül '  ' \" ile ayrınız. ",
                        max_length=255,
                        verbose_name="Anahtar Kelimeler",
                    ),
                ),
                ("aktif", models.BooleanField(default=True)),
                ("banner", models.BooleanField(default=False)),
                ("olusturma_tarihi", models.DateTimeField(auto_now_add=True)),
                ("guncelleme_tarihi", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name_plural": "Tüm Alt Kategoriler",},
        ),
        migrations.CreateModel(
            name="Siirler",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Şiirin başlığını girin.", max_length=255
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text="Şiirin URL'de görünecek kısmını girin.",
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "Model",
                    models.CharField(
                        choices=[
                            ("Şiirler", "Şiirler"),
                            ("Şairler", "Şairler"),
                            ("Sözler", "Sözler"),
                            ("Şarkı", "Şarkı"),
                            ("EnglishSiir", "EnglishSiir"),
                        ],
                        help_text="Modele göre sılanma ve konumlandırılma olacaktır.",
                        max_length=20,
                    ),
                ),
                (
                    "icerik",
                    ckeditor.fields.RichTextField(
                        blank=True, help_text="Şiirin içeriğini girin.", null=True
                    ),
                ),
                (
                    "hakkinda",
                    ckeditor.fields.RichTextField(
                        blank=True,
                        help_text="Şiir hakkında anlatılmak istenen.",
                        null=True,
                    ),
                ),
                (
                    "meta_description",
                    models.TextField(
                        blank=True,
                        help_text="Sayfanın meta açıklamasını girin.",
                        verbose_name="Meta Açıklama",
                    ),
                ),
                (
                    "keywords",
                    models.CharField(
                        blank=True,
                        help_text="Sayfanın anahtar kelimelerini \" Virgül '  ' \" ile ayrınız. ",
                        max_length=255,
                        verbose_name="Anahtar Kelimeler",
                    ),
                ),
                (
                    "kapak_resmi",
                    models.ImageField(
                        help_text="Anasayfa Resim",
                        upload_to=siirler.models.kapak_resmi_upload_to,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Taslak", "Taslak"),
                            ("Hazir", "Hazir"),
                            ("Yayinda", "Yayinda"),
                        ],
                        default="Taslak",
                        help_text="Şiirin durumunu seçin.",
                        max_length=10,
                    ),
                ),
                (
                    "aktif",
                    models.BooleanField(
                        default=True, help_text="Şiirin aktif olup olmadığını belirtin."
                    ),
                ),
                (
                    "banner",
                    models.BooleanField(
                        default=False,
                        help_text="Ana Sayfadaki büyük resim alanında ögrünür",
                    ),
                ),
                (
                    "small_banner",
                    models.BooleanField(
                        default=False, help_text="Ana sayfada küçük resimlerde görünür."
                    ),
                ),
                ("okunma_sayisi", models.PositiveIntegerField(default=0)),
                ("olusturma_tarihi", models.DateTimeField(auto_now_add=True)),
                ("guncelleme_tarihi", models.DateTimeField(auto_now=True)),
                (
                    "alt_kategorisi",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Şiirin alt kategorilerini seçin.",
                        to="siirler.siiraltkategori",
                    ),
                ),
                (
                    "sair",
                    models.ForeignKey(
                        help_text="Şiirin şairini seçin.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="sairler.sairler",
                    ),
                ),
                (
                    "yazar",
                    models.ForeignKey(
                        help_text="Şiiri yazan kullanıcıyı seçin.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name_plural": "Tüm Şiirler",},
        ),
    ]
