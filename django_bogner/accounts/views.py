from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.shortcuts import render, redirect
from .forms import SignUpForm


class SignUp(View):
    template_name = 'accounts/signup.html'

    def get(self, request):
        return render(request, self.template_name, {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.username = username
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('products:index')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')