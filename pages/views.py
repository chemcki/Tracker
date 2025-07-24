from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import TemplateView

# Temporary error view for docker ** DISABLE FOR PRODUCITON ** for debug=False
# def error_view(request):
#     raise Exception("This is a test exception")



class HomePageView(TemplateView):
    template_name ='home.html'

class DashboardPageView(TemplateView):
    template_name = "dashboard.html"