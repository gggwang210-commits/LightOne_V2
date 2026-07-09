from django.urls import reverse
from django.test import SimpleTestCase


class DashboardUrlTests(SimpleTestCase):
    def test_dashboard_url_resolves(self):
        self.assertEqual(reverse('dashboard:dashboard'), '/dashboard/')
