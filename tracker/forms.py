from django import forms
from django.utils import timezone
from .models import Habit, HabitRecord

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name"]

DUPLICATE_ERROR_MESSAGE = "This habit has already been recorded for this date."

class HabitRecordForm(forms.ModelForm):
    # Pre-fill date with today and allow user to change it
    date = forms.DateField(
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = HabitRecord
        fields = ["habit", "date", "description", "completed"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # only show habits for the current user
            self.fields['habit'].queryset = Habit.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean() 
        habit = cleaned_data.get("habit")
        date = cleaned_data.get("date")

        if habit and date:
            # Check for duplicate habit record
            if HabitRecord.objects.filter(habit=habit, date=date).exists():
                raise forms.ValidationError(DUPLICATE_ERROR_MESSAGE)
        
        return cleaned_data
    
    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        try:
            self.instance.validate_unique(exclude=exclude)
        except forms.ValidationError as e:
            # Remove Django's default __all__ error if present
            if '__all__' in e.error_dict:
                e.error_dict.pop('__all__')
            if e.error_dict:
                raise
        