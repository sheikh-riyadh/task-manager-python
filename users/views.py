from django.shortcuts import render
from users.forms import CustomUserRegistrationForm
from django.contrib.auth.models import User

# Create your views here.
def sign_up(request):
    form = CustomUserRegistrationForm()
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

    context={
        'form':form
    }
    return render(request, 'register/register.html',context)