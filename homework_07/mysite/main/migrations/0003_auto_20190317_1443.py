# Generated by Django 2.1.7 on 2019-03-17 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_department_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Адресс'),
        ),
    ]