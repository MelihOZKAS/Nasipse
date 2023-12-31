# Generated by Django 4.2.3 on 2023-08-04 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sozler", "0002_alter_sozler_okunma_sayisi_alter_sozler_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="YorumSozler",
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
                ("icerik", models.TextField()),
                ("olusturma_tarihi", models.DateTimeField(auto_now_add=True)),
                (
                    "soz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="yorumlar",
                        to="sozler.sozler",
                    ),
                ),
                (
                    "yazar",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FavoriSozler",
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
                ("olusturma_tarihi", models.DateTimeField(auto_now_add=True)),
                (
                    "kullanici",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "soz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sozler.sozler"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BegeniSozler",
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
                ("olusturma_tarihi", models.DateTimeField(auto_now_add=True)),
                (
                    "kullanici",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "soz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sozler.sozler"
                    ),
                ),
            ],
        ),
    ]
