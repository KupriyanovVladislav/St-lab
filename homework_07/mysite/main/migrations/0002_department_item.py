# Generated by Django 2.1.7 on 2019-03-17 11:18

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sphere', models.CharField(max_length=30, verbose_name='Направление')),
                ('staff_amount', models.PositiveIntegerField(verbose_name='Количество сотрудников')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Shop', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделы',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.PositiveIntegerField(verbose_name='Цены')),
                ('is_sold', models.BooleanField(verbose_name='Продано')),
                ('comments', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), size=None, verbose_name='Комментарии')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Department', verbose_name='Отдел')),
            ],
            options={
                'verbose_name': 'Предмет',
                'verbose_name_plural': 'Предметы',
            },
        ),
    ]
