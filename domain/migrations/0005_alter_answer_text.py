# Generated by Django 3.2.6 on 2021-10-26 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0004_auto_20211026_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
