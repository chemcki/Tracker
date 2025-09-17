
from django.test import TestCase
from django.contrib.auth import get_user_model
from tracker.models import Habit, HabitRecord
from datetime import date

User = get_user_model()

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='1234')
        self.habit = Habit.objects.create(user=self.user, name='Read')

    def test_habit_creation(self):
        self.assertEqual(self.habit.name, 'Read')
        self.assertEqual(self.habit.user.username, 'test')

class HabitRecordModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test2', password='1234')
        self.habit = Habit.objects.create(user=self.user, name='Run')

    def test_habit_record_creation(self):
        record = HabitRecord.objects.create(habit=self.habit, date=date.today(), completed=True)
        self.assertTrue(record.completed)
        self.assertEqual(record.habit.name, 'Run')


