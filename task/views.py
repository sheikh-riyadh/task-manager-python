from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def user_dashboard(req):
    return render(req, "dashboard/manager-dashboard.html")


def manager_dashboard(req):
    return render(req, "dashboard/user-dashboard.html")


def test(req):
    return render(req, "test.html")

