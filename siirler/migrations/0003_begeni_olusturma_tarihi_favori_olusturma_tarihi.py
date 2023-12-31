# Generated by Django 4.2.3 on 2023-08-03 21:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("siirler", "0002_siirler_aciklama_yorum_favori_begeni"),
    ]

    operations = [
        migrations.AddField(
            model_name="begeni",
            name="olusturma_tarihi",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="favori",
            name="olusturma_tarihi",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
