from django.contrib.auth.models import User
from django.shortcuts import render, redirect
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
        return render(request, 'users/login.html')


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        context = {'user': request.user}
        return render(request, 'users/profile.html', context)