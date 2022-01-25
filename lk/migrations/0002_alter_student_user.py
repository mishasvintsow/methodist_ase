# Generated by Django 3.2.6 on 2021-08-27 18:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('lk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.OneToOneField(limit_choices_to={'role__exact': 's'},
                                       on_delete=django.db.models.deletion.CASCADE, related_name='student',
                                       to=settings.AUTH_USER_MODEL),
        ),
    ]