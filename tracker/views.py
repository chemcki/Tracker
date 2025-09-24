from datetime import timedelta, datetime
from collections import defaultdict

from django.db.models import Q
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Habit, HabitRecord
from .forms import HabitForm, HabitRecordForm, SearchForm

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
    # Fetch records avoiding extra queries when accesing record.habit.name
    habit_records = HabitRecord.objects.select_related('habit')

     # sorting -- get sort query param; default is ascending by date
    sort = request.GET.get('sort', 'date') 
    if sort in ['date', '-date', 'habit__name', '-habit__name']:
        habit_records = habit_records.order_by(sort)

    # Grouping by habit
        group_by_habit = request.GET.get('group', None)
        if group_by_habit == 'habit':
            grouped_records = {}
            for record in habit_records:
                grouped_records.setdefault(record.habit, []).append(record)
            
            # Sort each habit's records by date (oldest to newest)
            for habit, records in grouped_records.items():
                records.sort(key=lambda r: r.date)
                
            context = {
                "grouped_records": grouped_records, 
                "grouped": True, 
                "sort": sort
                }
        else:
            # Pagination (for ungrouped lists)
            paginator = Paginator(habit_records, 15) # show 15 records per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                "habit_records": page_obj, 
                "grouped": False, 
                "sort": sort
                }
        return render(request, 'tracker/habit_record_list.html', context)


# class HabitRecordListView(LoginRequiredMixin, ListView):
#     model = HabitRecord
#     template_name = 'tracker/habit_record_list.html'
#     context_object_name = 'habit_record_list'

'''Create a single habit record for a particular date. Catches any duplicates
for the current date; if the form fails due to a duplicate, it ensures the 
DB rolls back cleanly with an error pop up '''

@login_required  
def habit_record_create(request):
    form = HabitRecordForm(request.POST or None, user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            try:
                with transaction.atomic():
            # habit_record = form.save(commit=False)
            # habit_record.user = request.user
                    habit_record = form.save()
                return redirect('record_detail', pk=habit_record.pk)
            except IntegrityError:
                # Only add error if form didn't already catch it
                # if not form.non_field_errors():
                    form._errors.clear()
                    form.add_error(None, "This habit has already been recorded for this date.")
        
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
    habit_records = HabitRecord.objects.filter(habit__in=habits, date__range=[start_date, end_date]
    )

    # Create a list of dates in the week
    week_dates = [start_date + timedelta(days=i) for i in range(7)]

    # Map habits to their records per day
    habit_status = {}

    for habit in habits:
        # Map date -> completed
        status_per_day = {}
        for date in week_dates:
            record = habit_records.filter(habit=habit, date=date).first()
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

# search for either dates habits were completed or habits and the dates they were completed
@login_required 
def search_results_list(request):
    form = SearchForm(request.GET or None)
    results = HabitRecord.objects.none()
    query = ""
    
    if form.is_valid():
        query = form.cleaned_data.get("q", "")
    
        if query:
            try:
                # Try to parse a date first
                search_date = datetime.strptime(query, "%Y-%m-%d").date()
                results = HabitRecord.objects.filter(date=search_date, completed=True) 
            except ValueError:
                # If not a date, treat as habit name
                results = HabitRecord.objects.filter(habit__name__icontains=query, completed=True)

    context = {"results": results, "query": query}
    return render(request, "tracker/search_results.html", context)


   