# Generated by Django 2.1.3 on 2018-12-02 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True)),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('max_guests', models.PositiveIntegerField(blank=True, null=True)),
                ('display_address', models.TextField()),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('approx_display_address', models.TextField()),
                ('approx_lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('approx_lng', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('protect_real_address', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True)),
                ('external_id', models.CharField(db_index=True, max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('full_name', models.TextField(blank=True)),
                ('short_name', models.TextField(blank=True)),
                ('picture', models.URLField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_layer.User'),
        ),
    ]
