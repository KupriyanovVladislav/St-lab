from django import forms
from .models import Department
from django.core.exceptions import ValidationError


CRITERIA_CHOICES = [
            (0, "Количество сотрудников в отделе"),
            (1, "Суммарная стоимость проданных товаров"),
            (2, "Суммарная стоимость не проданных товаров"),
            (3, "Суммарная стоимость всех товаров"),
            (4, "Количество проданных товаров"),
            (5, "Количество не проданных товаров"),
            (6, "Количество всех товаров")
        ]


class ComparedDepartmentsForm(forms.Form):
    main = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        label="Выберите отдел:"
    )
    secondary = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        label="Выберите отдел:"
    )
    criteria = forms.MultipleChoiceField(
        choices=CRITERIA_CHOICES,
        label="Критерии",
        required=True,
    )

    def clean(self):
        if self.data.get('main') == self.data.get('secondary'):
            raise ValidationError('Выберите другой магазин')
        super().clean()

