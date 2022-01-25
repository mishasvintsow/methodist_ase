# Generated by Django 3.2.6 on 2021-09-14 12:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('lk', '0003_teacher_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[('r', 'Суперпользователь'), ('m', 'Методист'), ('t', 'Учитель'), ('a', 'Аудитор'),
                         ('s', 'Студент'), ('n', 'Аноним')], default='n', help_text='User role', max_length=1),
        ),
    ]