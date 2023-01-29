from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from users.forms import UserCreateForm

# Create your views here.


class RegisterView(View):
    def get(self, request):
        user_form = UserCreateForm()
        context = {'form': user_form}
        return render(request, 'users/register.html', context=context)

    def post(self, request):
        user_form = UserCreateForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
        # print(f"{username}  {password}")
        else:
            context = {'form': user_form}
            return render(request, 'users/register.html', context=context)

        return redirect('users:login')


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {'login_form': login_form}
        return render(request, 'users/login.html', context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
        else:
            return render(request, 'users/login.html', {'login_form': login_form})
        return redirect('books:list')


class LogOutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have successfully logged out!')
        return redirect('landing_page')


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        context = {'user': request.user}
        return render(request, 'users/profile.html', context)