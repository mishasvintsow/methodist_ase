# Generated by Django 3.2.6 on 2022-01-18 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lk', '0006_auto_20220117_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.IntegerField(choices=[(5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11')], default=5, verbose_name='Класс'),
        ),
        migrations.AlterField(
            model_name='student',
            name='pause',
            field=models.BooleanField(default=False, verbose_name='Пауза'),
        ),
        migrations.AlterField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='lk.teacher', verbose_name='Преподаватель'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('r', 'Суперпользователь'), ('m', 'Методист'), ('t', 'Учитель'), ('a', 'Аудитор'), ('s', 'Студент'), ('n', 'Аноним')], default='n', max_length=1, verbose_name='Роль пользователя'),
        ),
    ]
