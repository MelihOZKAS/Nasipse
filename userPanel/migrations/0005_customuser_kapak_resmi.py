# Generated by Django 4.2.3 on 2023-08-12 18:23

from django.db import migrations, models
import userPanel.models


class Migration(migrations.Migration):

    dependencies = [
        ("userPanel", "0004_customuser_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="kapak_resmi",
            field=models.ImageField(
                blank=True, null=True, upload_to=userPanel.models.kapak_resmi_upload_to
            ),
        ),
    ]
