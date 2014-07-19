from django.core.urlresolvers import reverse
from django.test import TestCase


class EasterEggTestCase(TestCase):
    def test_index_page_returns_200(self):
        url = reverse('index')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)


class CoverageTestCase(TestCase):
    def test(self):
        from easter_egg import wsgi
        assert wsgi
