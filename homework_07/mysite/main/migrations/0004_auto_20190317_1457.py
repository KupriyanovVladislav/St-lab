# Generated by Django 2.1.7 on 2019-03-17 11:57

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190317_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='comments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), size=None),
        ),
    ]
