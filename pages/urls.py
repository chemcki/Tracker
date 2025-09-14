from django.urls import path

from .views import HomePageView
from tracker.views import dashboard


urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('', HomePageView.as_view(), name='home'),
] 