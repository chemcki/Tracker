from django.conf import settings
from django.db import models
from django.utils import timezone


"""
Lists a habit name links it to a logged in user

"""

class Habit(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    # created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

"""
Records what habit was accomplished and when, and establishes one 
habit has only one record per date.

"""

class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date =  models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ["habit", "date"]

    def __str__(self):
        return f"{self.habit.name} on {self.date}"