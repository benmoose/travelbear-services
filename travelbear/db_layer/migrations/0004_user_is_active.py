# Generated by Django 2.1.5 on 2019-02-07 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_layer', '0003_trip_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
