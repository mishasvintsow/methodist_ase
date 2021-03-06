# Generated by Django 3.2.6 on 2021-11-04 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lk', '0004_alter_user_role'),
        ('domain', '0005_alter_answer_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IID', models.IntegerField(unique=True)),
                ('response', models.CharField(max_length=256, null=True)),
                ('valid', models.BooleanField(default=None)),
                ('status', models.CharField(choices=[('n', 'Ответ отсутствует'), ('r', 'Правильно'), ('c', 'Неправильно, понятно'), ('u', 'Неправильно, не понятно'), ('d', 'Затруднение с ответом'), ('i', 'Некорректный ответ'), ('w', 'Проработано')], default='n', max_length=1)),
                ('time_start', models.DateTimeField(null=True)),
                ('time_finish', models.DateTimeField(null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_items', to='domain.task')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MID', models.IntegerField(unique=True)),
                ('status', models.CharField(choices=[('i', 'Не актуально'), ('l', 'Изучение'), ('r', 'Закрепление'), ('d', 'Удалено из программы')], default='i', max_length=1)),
                ('order', models.IntegerField(null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='lk.student')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domain.topic')),
            ],
            options={
                'ordering': ['student__SID', 'order'],
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TID', models.IntegerField(unique=True)),
                ('status', models.CharField(choices=[('u', 'Неопределенный'), ('n', 'Создан'), ('o', 'Открыт'), ('s', 'Начат'), ('f', 'Выполнен'), ('c', 'Истек')], default='n', max_length=1)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_open', models.DateTimeField(null=True)),
                ('time_start', models.DateTimeField(null=True)),
                ('time_finish', models.DateTimeField(null=True)),
                ('time_close', models.DateTimeField(null=True)),
                ('dev', models.BooleanField(default=False)),
                ('practice', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(through='study.Item', to='domain.Task')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='lk.student')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UID', models.IntegerField(unique=True)),
                ('status', models.CharField(choices=[('l', 'Изучение'), ('r', 'Закрепление')], default='r', max_length=1)),
                ('order', models.IntegerField()),
                ('complete', models.BooleanField(default=False)),
                ('duration', models.IntegerField(default=1)),
                ('time_start', models.DateTimeField(null=True)),
                ('time_finish', models.DateTimeField(null=True)),
                ('min_item', models.IntegerField(default=3)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.test')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domain.topic')),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='units',
            field=models.ManyToManyField(through='study.Unit', to='domain.Topic'),
        ),
        migrations.CreateModel(
            name='ModuleHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('switch', models.CharField(choices=[('ar', 'Добавить в "Повторение"'), ('al', 'Добавить в "Изучение"'), ('ai', 'Добавить в "Не актуально"'), ('rd', 'Удалить из "Повторение"'), ('ld', 'Удалить из "Изучение"'), ('id', 'Удалить из "Не актуально"'), ('rl', 'Переключить из "Повторение" в "Изучение"'), ('ri', 'Переключить из "Повторение" в "Не актуально"'), ('lr', 'Переключить из "Изучение" в "Повторение"'), ('li', 'Переключить из "Изучение" в "Не актуально"'), ('il', 'Переключить из "Не актуально" в "Изучение"'), ('ir', 'Переключить из "Не актуально" в "Повторение"')], default='ai', help_text='Switch status of module', max_length=2)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.module')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_items', to='study.test'),
        ),
    ]
