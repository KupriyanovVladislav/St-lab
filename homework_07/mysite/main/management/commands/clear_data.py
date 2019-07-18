from django.core.management.base import BaseCommand, CommandError
from main.models import Shop, Department, Item


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            Shop.objects.all().delete()
            Department.objects.all().delete()
            Item.objects.all().delete()
        except Shop.DoesNotExist:
            raise CommandError("Shop doesn't exist")
        except Department.DoesNotExist:
            raise CommandError("Department doesn't exist")
        except Item.DoesNotExist:
            raise CommandError("Item doesn't exist")
