# Generated by Django 5.0.6 on 2024-07-09 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('phone', models.CharField(max_length=255, verbose_name='Телефон')),
                ('blocked', models.BooleanField(default=False, verbose_name='Заблокирован')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('avatar', models.URLField(verbose_name='Ссылка на аватар')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('score', models.IntegerField(verbose_name='Оценка (1-5)')),
                ('rated', models.CharField(max_length=255, verbose_name='Дата публикации отзыва')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Works',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Ссылка на картинку')),
            ],
            options={
                'verbose_name': 'Мои работы',
                'verbose_name_plural': 'Мои работы',
            },
        ),
        migrations.CreateModel(
            name='Window',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Окошко')),
                ('done', models.BooleanField(default=False, verbose_name='Выполнено')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='windows', to='main.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Окошко',
                'verbose_name_plural': 'Окошки',
            },
        ),
    ]
