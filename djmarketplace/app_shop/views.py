from django.views.generic import ListView
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView


class MainView(ListView): #4
    model = Good
    queryset = Good.objects.all()
    template_name = 'app_shop/main.html'

class CustomLoginView(LoginView): #2
    template_name = 'app_shop/login.html'
    next_page = 'main'

    def form_valid(self, form):
        responce = super(CustomLoginView, self).form_valid(form)
        return responce

class CustomLogoutView(LogoutView): #3
    template_name = 'app_shop/logout.html'
    next_page = 'main'

def register_view(request): #1

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            Profile.objects.create(user=user)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)
            return redirect('main')
        return render(request, 'app_shop/register.html', context={'user_form': user_form, 'errors': user_form.error_messages})
    else:
        user_form = UserForm()
        return render(request, 'app_shop/register.html', context={'user_form': user_form})