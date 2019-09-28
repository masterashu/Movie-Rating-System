from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, SignupForm
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
User = get_user_model()


def home(request):
    return render(request, 'accounts/home.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                auth_login(request, user)
                return render(request, 'accounts/profile.html', context={'user': request.user})
            else:
                error = 'Wrong Password or User Doesn\'t exist.'
                return render(request, 'accounts/login.html', context={'error': error, 'form': form})
        else:
            error = 'Wrong Information'
            return render(request, 'accounts/login.html', context={'error': error, 'form': form})
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', context={'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = request.POST['username']
            user.set_password(request.POST['password'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.mobile = request.POST['mobile']
            user.save()
            return HttpResponseRedirect('home')
        else:
            if request.POST['password'] != request.POST['password2']:
                error = 'Passwords Do Not Match'
            else:
                error = 'Username is Taken'
            return render(request, 'accounts/signup.html', context={'error': error, 'form': form})
    else:
        form = SignupForm()
        return render(request, 'accounts/signup.html', context={'form': form})


def logout(request):
    auth_logout(request)
    form = LoginForm()
    return render(request, 'accounts/login.html', context={'form': form, 'logout_message': 'Logged Out Successfully'})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', context={'user': request.user})
