from django.shortcuts import redirect
from .models import Mark


class CheckConditionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        conditions = [
            Mark.objects.count() >= 20,
            not request.path.startswith('/admin/'),
            request.path != '/disabled/'
        ]

        if all(conditions):
            return redirect('disabled')

        response = self.get_response(request)
        return response
