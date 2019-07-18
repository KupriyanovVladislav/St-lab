from .models import Item


def active_items(request):
    return {'ITEMS_AMOUNT': Item.objects.filter(is_sold=False).count()}
