# Generated by Django 3.2.6 on 2022-01-05 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('study', '0003_auto_20220104_1853'),
        ('domain', '0005_alter_answer_text'),
        ('lk', '0004_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_A', models.IntegerField(default=0)),
                ('unit_AL', models.FloatField(default=0)),
                ('unit_T', models.IntegerField(default=0)),
                ('unit_TL', models.FloatField(default=0)),
                ('unit_P', models.FloatField(default=0)),
                ('unit_D', models.FloatField(default=0)),
                ('unit_R', models.FloatField(default=0)),
                ('unit_E', models.FloatField(default=0)),
                ('unit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='study.unit')),
            ],
        ),
        migrations.CreateModel(
            name='TopicFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_A', models.IntegerField(default=0)),
                ('topic_T', models.IntegerField(default=0)),
                ('topic_L', models.FloatField(default=0)),
                ('topic', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='domain.topic')),
            ],
        ),
        migrations.CreateModel(
            name='TestFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_A', models.IntegerField(default=0)),
                ('test_AL', models.FloatField(default=0)),
                ('test_T', models.IntegerField(default=0)),
                ('test_TL', models.FloatField(default=0)),
                ('test_P', models.FloatField(default=0)),
                ('test_D', models.FloatField(default=0)),
                ('test_R', models.FloatField(default=0)),
                ('test_E', models.FloatField(default=0)),
                ('test', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='study.test')),
            ],
        ),
        migrations.CreateModel(
            name='TaskFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_A', models.IntegerField(default=0)),
                ('task_T', models.IntegerField(default=0)),
                ('task_L', models.FloatField(default=0)),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='domain.task')),
            ],
        ),
        migrations.CreateModel(
            name='StudentFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_A', models.IntegerField(default=0)),
                ('student_AL', models.FloatField(default=0)),
                ('student_T', models.IntegerField(default=0)),
                ('student_TL', models.FloatField(default=0)),
                ('student_P', models.FloatField(default=0)),
                ('student_D', models.FloatField(default=0)),
                ('student_R', models.FloatField(default=0)),
                ('student_E', models.FloatField(default=0)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lk.student')),
            ],
        ),
        migrations.CreateModel(
            name='ModuleFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_A', models.IntegerField(default=0)),
                ('module_AL', models.FloatField(default=0)),
                ('module_T', models.IntegerField(default=0)),
                ('module_TL', models.FloatField(default=0)),
                ('module_P', models.FloatField(default=0)),
                ('module_D', models.FloatField(default=0)),
                ('module_R', models.FloatField(default=0)),
                ('module_E', models.FloatField(default=0)),
                ('module', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='study.module')),
            ],
        ),
        migrations.CreateModel(
            name='ItemFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_A', models.IntegerField(default=0)),
                ('task_T', models.IntegerField(default=0)),
                ('task_L', models.FloatField(default=0)),
                ('topic_A', models.IntegerField(default=0)),
                ('topic_T', models.IntegerField(default=0)),
                ('topic_L', models.FloatField(default=0)),
                ('student_A', models.IntegerField(default=0)),
                ('student_AL', models.FloatField(default=0)),
                ('student_T', models.IntegerField(default=0)),
                ('student_TL', models.FloatField(default=0)),
                ('student_P', models.FloatField(default=0)),
                ('student_D', models.FloatField(default=0)),
                ('student_R', models.FloatField(default=0)),
                ('student_E', models.FloatField(default=0)),
                ('module_A', models.IntegerField(default=0)),
                ('module_AL', models.FloatField(default=0)),
                ('module_T', models.IntegerField(default=0)),
                ('module_TL', models.FloatField(default=0)),
                ('module_P', models.FloatField(default=0)),
                ('module_D', models.FloatField(default=0)),
                ('module_R', models.FloatField(default=0)),
                ('module_E', models.FloatField(default=0)),
                ('test_A', models.IntegerField(default=0)),
                ('test_AL', models.FloatField(default=0)),
                ('test_T', models.IntegerField(default=0)),
                ('test_TL', models.FloatField(default=0)),
                ('test_P', models.FloatField(default=0)),
                ('test_D', models.FloatField(default=0)),
                ('test_R', models.FloatField(default=0)),
                ('test_E', models.FloatField(default=0)),
                ('unit_A', models.IntegerField(default=0)),
                ('unit_AL', models.FloatField(default=0)),
                ('unit_T', models.IntegerField(default=0)),
                ('unit_TL', models.FloatField(default=0)),
                ('unit_P', models.FloatField(default=0)),
                ('unit_D', models.FloatField(default=0)),
                ('unit_R', models.FloatField(default=0)),
                ('unit_E', models.FloatField(default=0)),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='study.item')),
            ],
        ),
    ]
