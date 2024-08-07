# Generated by Django 5.0.6 on 2024-07-13 15:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_user_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="bio",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="user",
            name="description",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.CreateModel(
            name="Relation",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "from_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following_relations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "to_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="follower_relations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "relation",
                "verbose_name_plural": "relations",
            },
        ),
    ]
