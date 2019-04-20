from django import template
from main.forms import CRITERIA_CHOICES
from main.views import ComparedDepartmentsView

register = template.Library()


@register.simple_tag
def department_leader(main, secondary, criterion: str):
    criteria_dict = dict(CRITERIA_CHOICES)

    for key in criteria_dict.keys():
        if criteria_dict.get(key) == criterion:
            criterion_id = key
            break
    else:
        return None

    result_main = ComparedDepartmentsView.choice_filter(main, criterion_id)
    result_secondary = ComparedDepartmentsView.choice_filter(secondary, criterion_id)

    if result_main >= result_secondary:
        return main
    else:
        return secondary
