from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

from registration.models import CustomUser
from task1.forms import UserLoginForm, UserCreateForm


def CreateView(request):
    if request.method == 'GET':
        form = UserCreateForm()
    else:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = CustomUser(username=form.cleaned_data['username'],
                              password=make_password(form.cleaned_data['password1']))
            user.save()
            request.session['userid'] = str(user.id)
            login(request, user)
            return HttpResponseRedirect(redirect_to=reverse('registration:edit'))
    return render(request, 'accounts/signup.html', {'form': form})


def SignUpView(request):
    if request.method == 'GET':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = CustomUser(username=form.cleaned_data['username'],
                              password=make_password(form.cleaned_data['password1']))
            user.save()
            request.session['userid'] = str(user.id)
            login(request, user)
            return HttpResponseRedirect(redirect_to=reverse('registration:edit'))
    return render(request, 'accounts/signup.html', {'form': form})


def LoginView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=reverse('registration:details'))
    if request.method == 'GET':
        form = UserLoginForm()
    else:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user and user.is_active:
                request.session['userid'] = str(user.id)
                login(request, user)
                return HttpResponseRedirect(redirect_to=reverse('registration:details'))
    return render(request, 'accounts/login.html', {'form': form})


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse('login'))
