from django.test import TestCase
from django.contrib.auth import get_user_model
from tracker.forms import HabitForm, HabitRecordForm
from tracker.models import Habit, HabitRecord
from datetime import date

User = get_user_model()


class HabitFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234')

    def test_habit_form_valid_data(self):
        form = HabitForm(data={
            "name": "Read",
        })
        self.assertTrue(form.is_valid())

    def test_habit_form_invalid_data(self):
        # Name is required, so empty data should fail
        form = HabitForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

class HabitRecordFormTest(TestCase):
    def setUp(self):
        self.user= User.objects.create_user(username='testuser2', password='1234')
        self.habit = Habit.objects.create(user=self.user, name='Run')

    def test_habit_record_form_valid_data(self):
        form = HabitRecordForm(data={
            "habit": self.habit.id,
        })
        self.assertTrue(form.is_valid())

    def test_habit_record_form_invalid_data(self):
        # Missing habit or date should fail
        form = HabitRecordForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('habit', form.errors)
        