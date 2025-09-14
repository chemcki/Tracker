from datetime import timedelta
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Habit, HabitRecord
from .forms import HabitForm, HabitRecordForm

@login_required    
def habit_list(request):
    habits = Habit.objects.all()
    context = {'habits': habits}
    return render(request, 'tracker/habit_list.html', context)
    

# class HabitListView(LoginRequiredMixin, ListView):
#      model = Habit
#      template_name = "tracker/habit_list.html"
#      context_object_name = "habits"

@login_required  
def habit_create(request):
    form = HabitForm(request.POST or None)
    if form.is_valid():
        habit = form.save(commit=False)
        habit.user = request.user
        habit.save()
        return redirect('habit_list')
    
    context = {'form': form}
    return render(request, 'tracker/habit_form.html', context)

# class HabitCreateView(LoginRequiredMixin, CreateView):
#      model = Habit
#      form_class = HabitForm
#      template_name = "tracker/habit_form.html"
#      success_url = reverse_lazy("habit_list")

#      def form_valid(self, form):
#           form.instance.user = self.request.user
#           return super().form_valid(form)

@login_required  
def habit_update(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    form = HabitForm(request.POST or None, instance=habit)
    if form.is_valid():
        form.save()
        return redirect('habit_list')
    
    context = {'form': form}
    return render(request, 'tracker/habit_form.html', context)

# class HabitUpdateView(LoginRequiredMixin, UpdateView):
#      model = Habit
#      form_class = HabitForm
#      template_name = 'tracker/habit_form.html'
#      success_url = reverse_lazy("habit_list")

@login_required  
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if request.method == "POST":
        habit.delete()
        return redirect("habit_list")

    context = {"habit": habit}
    return render(request, "tracker/habit_confirm_delete.html", context)

# class HabitDeleteView(LoginRequiredMixin, DeleteView):
#      model = Habit
#      template_name = 'tracker/habit_confirm_delete.html'
#      success_url = reverse_lazy("habit_list")

@login_required  
def habit_record_list(request):
     habit_records = HabitRecord.objects.all()
     context = {"habit_records": habit_records}
     return render(request, 'tracker/habit_record_list.html', context)


# class HabitRecordListView(LoginRequiredMixin, ListView):
#     model = HabitRecord
#     template_name = 'tracker/habit_record_list.html'
#     context_object_name = 'habit_record_list'


@login_required  
def habit_record_create(request):
    form = HabitRecordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            habit_record = form.save(commit=False)
            habit_record.user = request.user
            habit_record.save()
            return redirect('record_detail', pk=habit_record.pk)
        
    context = {'form': form}
    return render(request, 'tracker/habit_record_form.html', context)

# class HabitRecordCreate(LoginRequiredMixin, CreateView):
#     model = HabitRecord
#     form_class = HabitRecordForm
#     template_name = 'tracker/habit_record_form.html'
#     success_url = reverse_lazy('habit_record_list')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)



@login_required  
def habit_record_detail(request, pk):
    habit_record = get_object_or_404(HabitRecord, pk=pk)

    context = {"habit_record": habit_record}
    return render(request, 'tracker/habit_record_detail.html', context)

# class HabitRecordDetailView(LoginRequiredMixin, DetailView):
#     model = HabitRecord
#     template_name = 'tracker/habit_record_detail.html'
#     context_object_name = "habit_record"

@login_required  
def habit_record_update(request, pk):
    habit_record = get_object_or_404(HabitRecord, pk=pk)
    form = HabitRecordForm(request.POST or None, instance=habit_record, user=request.user)
    if form.is_valid():
        form.save()
        return redirect('record_detail', pk=habit_record.pk)

    context = {
        "form": form,
        "habit_record": habit_record,
    }
               
    return render(request, 'tracker/habit_record_form.html', context)

# class HabitRecordUpdateView(LoginRequiredMixin, UpdateView):
#     model = HabitRecord
#     form_class = HabitRecordForm
#     template_name = "tracker/habit_record_form.html"
#     success_url = reverse_lazy('habit_record_detail', 'pk': self:object.pk) 

@login_required  
def habit_record_delete(request, pk):
    habit_record = get_object_or_404(HabitRecord, pk=pk)
    if request.method == 'POST':
        habit_record.delete()
        return redirect('habit_record')
    context = {"habit_record": habit_record}
    return render(request, 'tracker/habit_record_delete.html', context)

# class HabitRecordDelete(LoginRequiredMixin, DeleteView):
    # model = HabitRecord
    # template_name = 'tracker/habit_record_confirm_delete.html'
    # success_url = reverse_lazy("habit_record")

@login_required  
def dashboard(request):
    # Get only the current user's habits
    habits = Habit.objects.filter(user=request.user)

    # Calculate this week's monday
    today = timezone.now().date()
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)

    # Get week offset from query param (?week=-1 for last week, ?week=1 for next week)
    week_offset = int(request.GET.get("week", 0))
    start_date = start_date + timedelta(weeks=week_offset)
    end_date = start_date + timedelta(days=6)

    # Get the records in that window
    habit_records = HabitRecord.objects.filter(habit__in=habits, date__date__range=[start_date, end_date]
    )

    # Create a list of dates in the week
    week_dates = [start_date + timedelta(days=i) for i in range(7)]

    # Map habits to their records per day
    habit_status = {}

    for habit in habits:
        # Map date -> completed
        status_per_day = {}
        for date in week_dates:
            record = habit_records.filter(habit=habit, date__date=date).first()
            status_per_day[date] = record.completed if record else False
        habit_status[habit] = status_per_day

    context = { 
        "habits": habits,
        "habit_records": habit_records,
        "habit_status": habit_status,
        "week_dates": week_dates,
        "start_date": start_date,
        "end_date": end_date,
        "today": today,
        "week_offset": week_offset,
    }
    
    return render(request, 'dashboard.html', context)

# class DashboardPageView(LoginRequiredMixin, TemplateView):
#   template_name = "dashboard.html"

#   def get_context_date(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#       habits = Habit.objects.filter(user=self.request.user)
#       
#       today = timezone.now().date()
#       start_date = today - timedelta(days=6)
#       
#       habit_records = HabitRecord.objects.filter(habit__in=habits, date__date__range=[start_date, today])

#       context.update({
#             'habits': habits,
#             'habit_records': habit_records,
#             'start_date': start_date,
#             'today': today,
#       })
#       return context
