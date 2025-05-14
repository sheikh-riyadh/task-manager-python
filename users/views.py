from django.shortcuts import render, redirect, HttpResponse
from users.forms import CustomUserRegistrationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from users.forms import LoginForm, AssignRoleForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator


# Create your views here.
def sign_up(request):
    form = CustomUserRegistrationForm()
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active=False
            user.save()
            messages.success(request, 'Please check your email for activation.')

    context={
        'form':form
    }
    return render(request, 'register/register.html',context)

def sign_in(request): 
    form = LoginForm(request)
    if request.method == 'POST': 
        form = LoginForm(request, data=request.POST) 
        if form.is_valid(): 
            user = form.get_user()
            login(request, user)
            return redirect('home') 
     
    context = {'form': form}
    return render(request, 'signin/signin.html', context)



def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign-in')
    

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid token or id')
    except:
        return HttpResponse('User not found')


def admin_dashboard(request):
    users  = User.objects.all()
    context={
        'users' : users
    }
    return render(request, 'admin/dashboard.html', context)

def assign_role(request, user_id):
    form = AssignRoleForm()
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # Remove old group
            user.groups.add(role)
            messages.success(request, f'User {user.username} has been assigned to the {role.name} ')
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {'form':form})
