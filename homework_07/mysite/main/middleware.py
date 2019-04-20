from django.shortcuts import redirect

from .models import Item
from .models import Statistics


class CheckConditionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        active_items = Item.objects.filter(is_sold=False).count()

        conditions = [
            active_items == 0,
            not request.path.startswith('/admin/'),
            request.path != '/disabled/'
        ]

        if all(conditions):
            return redirect('disabled')

        response = self.get_response(request)

        return response


class StatisticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        statistics = Statistics.objects.get_or_create(url=request.path)
        statistics[0].amount += 1
        statistics[0].save()

        response = self.get_response(request)

        return response
