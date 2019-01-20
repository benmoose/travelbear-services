# Generated by Django 2.1.4 on 2019-01-20 09:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [("db_layer", "0002_location_move")]

    operations = [
        migrations.CreateModel(
            name="TripMember",
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
                    "trip_member_id",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="db_layer.Trip"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="db_layer.User"
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="tripmember", unique_together={("trip", "user")}
        ),
    ]
