from django.contrib.postgres.fields import ArrayField
from django.db import models


class Shop(models.Model):
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name

    name = models.CharField(max_length=30, verbose_name='Название')
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name='Адресс')
    staff_amount = models.PositiveIntegerField(verbose_name='Количество сотрудников')


class Department(models.Model):
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return f'{self.sphere}'

    sphere = models.CharField(max_length=30, verbose_name='Направление')
    staff_amount = models.PositiveIntegerField(verbose_name='Количество сотрудников')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин', related_name='departments')


class Item(models.Model):
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return f'{self.name}'

    name = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    is_sold = models.BooleanField(verbose_name='Продано')
    comments = ArrayField(models.CharField(max_length=50), blank=True, verbose_name="Комментарии")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Отдел', related_name='items')


class Statistics(models.Model):
    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'

    url = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.amount} - {self.url}'
