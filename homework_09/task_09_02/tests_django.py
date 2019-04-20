from django.test import TestCase
from .models import Item


class ProjectTest(TestCase):
    urls_302 = ["/compare/departments/", "/1/", "1/2/addItem/", "2/4/updateDepartment/"]
    urls_200 = ["/disabled/", ]

    def test_urls(self):
        for url in self.urls_302:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

        for url in self.urls_200:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_disable(self):
        unsold_items = Item.objects.filter(is_sold=True)
        for item in unsold_items:
            item.delete()

        response = self.client.get('')

        self.assertRedirects(response, expected_url='/disabled/')
