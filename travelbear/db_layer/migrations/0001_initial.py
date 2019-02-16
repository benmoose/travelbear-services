# Generated by Django 2.1.3 on 2018-12-03 14:30

import uuid

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Trip",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_on", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "trip_id",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("title", models.TextField()),
                ("description", models.TextField(blank=True)),
                (
                    "tags",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, null=True
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_on", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "user_id",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "external_id",
                    models.CharField(db_index=True, max_length=255, unique=True),
                ),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("full_name", models.TextField(blank=True)),
                ("short_name", models.TextField(blank=True)),
                ("picture", models.URLField(blank=True)),
            ],
            options={"abstract": False},
        ),
        migrations.AddField(
            model_name="trip",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="db_layer.User"
            ),
        ),
    ]
