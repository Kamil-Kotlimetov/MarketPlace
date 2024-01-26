from django.views.generic import ListView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserForm, CartAddForm
from django.db.models import Avg
from django.urls import reverse
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView


class UserUpdateView(UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'app_shop/profile.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})

class MainView(ListView): #4
    model = Good
    queryset = Good.objects.select_related('shop', 'category').defer('amount', 'activity_flag').filter(amount__gt=0, activity_flag='a')
    context_object_name = 'goods'
    template_name = 'app_shop/main.html'

    def get_context_data(self, *, object_list=None, **kwargs): #5
        context = super(MainView, self).get_context_data(**kwargs)
        context['avg_price'] = Good.objects.only('price').aggregate(avg_price=Avg('price')).get('avg_price')
        context['add_form'] = CartAddForm()
        return context

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