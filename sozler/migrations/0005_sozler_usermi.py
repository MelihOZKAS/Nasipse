# Generated by Django 4.2.3 on 2023-08-11 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sozler", "0004_alter_sozler_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="sozler",
            name="usermi",
            field=models.BooleanField(default=False),
        ),
    ]
