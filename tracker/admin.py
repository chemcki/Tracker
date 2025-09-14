from django.contrib import admin

from .models import Habit, HabitRecord

class HabitRecordAdmin(admin.ModelAdmin):
    list_display = ("habit", "date", "completed")

admin.site.register(Habit)
admin.site.register(HabitRecord, HabitRecordAdmin)
