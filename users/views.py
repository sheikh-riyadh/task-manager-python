from django.shortcuts import render, redirect
from users.forms import CustomUserRegistrationForm
from django.contrib.auth import authenticate, login, logout

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

def sign_in(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
    
    return render(request, 'signin/signin.html')


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign-in')
