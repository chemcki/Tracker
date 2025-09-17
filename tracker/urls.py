from django.urls import path

from . import views

urlpatterns = [
    path('search_results/', views.search_results_list, name= 'search_results'),
    path("", views.habit_list, name="habit_list"),
    path('new/', views.habit_create, name='habit_create'),
    path('<int:pk>/edit/', views.habit_update, name='habit_update'),
    path('<int:pk>/delete/', views.habit_delete, name='habit_delete'),
    path('habit_record/', views.habit_record_list, name='habit_record'),
    path('record_new/', views.habit_record_create, name='record_new'),
    path('record/<int:pk>/detail/', views.habit_record_detail, name='record_detail'),
    path('record/<int:pk>/edit/', views.habit_record_update, name='record_update'),
    path('record/<int:pk>/delete/', views.habit_record_delete, name='record_delete'), 
]