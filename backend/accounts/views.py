"""
Accounts Views
"""

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View

from . import forms


class LoginView(View):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        return render(request, self.template_name, {"form" : form})

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    user_name = user.username
                    return HttpResponseRedirect(
                        reverse('bitcoin_arbitrage:realtime')
                    )
                else:
                    messages.error(request, 'That user account has been disabled')
            else:
                messages.error(request, "Username or password is incorrect.")
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('accounts:login'))


class MyProfileView(LoginRequiredMixin, View):
    template_name = "my-profile.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
