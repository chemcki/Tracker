from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone           
from tracker.models import Habit, HabitRecord
from tracker.views import search_results_list
from django.contrib.auth import get_user_model

User = get_user_model()

class HabitRecordSearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.client = Client()
        self.client.login(username="testuser", password="pass")

        self.habit1 = Habit.objects.create(name="Walked", user=self.user)
        self.habit2 = Habit.objects.create(name="Coding", user=self.user)

        self.record1 = HabitRecord.objects.create(
            habit=self.habit1, date="2025-09-16",description="Morning walk", completed=True
        )

        self.record2 = HabitRecord.objects.create(
            habit=self.habit2, date="2025-09-16", description="Code session", completed=True
        )

    def test_search_by_date_dash(self):
        response = self.client.get(reverse("search_results") + "?q=2025-09-16")
        self.assertContains(response, "Walked")
        self.assertContains(response,"Coding")

    def test_search_by_habit_name_case_insensitive(self):
        response = self.client.get(reverse("search_results") + "?q=walked")
        self.assertContains(response, "Walked")

    def test_search_by_habit_name_partial(self):
        response = self.client.get(reverse("search_results") + "?q=Walk")

    def test_search_invalid_date_format(self):
        response = self.client.get(reverse("search_results") + "?q=2025 09 16")
        # Should return no results or error message
        self.assertContains(response, "No results found", status_code = 200)