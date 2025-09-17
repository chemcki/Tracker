from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from .views import HomePageView
from tracker.views import dashboard

User = get_user_model()

class HomepageTests(TestCase):
    def setUp(self):
         # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Log in the user
        self.client.login(username='testuser', password='testpass')
        url = reverse("home")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "home.html")

    def test_hommepage_contains_correct_html(self):
        self.assertContains(self.response, "homepage")

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "This shouldn't show up on page!")

    def test_homepage_url_resolves_homepageview(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)

class DashboardPageTests(TestCase):
    def setUp(self):
         # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Log in the user
        self.client.login(username='testuser', password='testpass')
        # Get Dashboard page
        url = reverse("dashboard")
        self.response = self.client.get(url)

    def test_dashboardpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_dashboardpage_template(self):
        self.assertTemplateUsed(self.response, "dashboard.html")

    def test_dashboardpage_contains_correct_html(self):
        self.assertContains(self.response, "Dashboard")

    def test_dashboardpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "I'm not found on the page")

    def test_dashboardpage_url_resolves_dashboardpageview(self):
        view = resolve("/dashboard")
        self.assertEqual(view.func.__name__,dashboard.__name__)