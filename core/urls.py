from django.urls import path
from core.views import home
from users.views import sign_out

urlpatterns = [
    path('', home, name='home'),
    path('sign-out', sign_out, name="sing-out" )
]