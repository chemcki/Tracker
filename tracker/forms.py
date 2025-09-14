from django import forms
from .models import Habit, HabitRecord

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name"]

class HabitRecordForm(forms.ModelForm):
    class Meta:
        model = HabitRecord
        fields = ["habit", "description", "completed"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['habit'].queryset = Habit.objects.filter(user=user)
        