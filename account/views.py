from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login, authenticate as auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormView

from quiz.models import Note
from .forms import LoginForm, RegisterForm
from ktn.views import try_next


class Login(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        login(self.request, auth(username=form.cleaned_data['username'], password=form.cleaned_data['password']))
        return try_next(self.request, self.success_url)


class Register(FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        login(self.request, form.save(self.request))
        return try_next(self.request, self.success_url)


class Logout(View):
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logout(request)

        return HttpResponseRedirect(self.success_url)


class Account(LoginRequiredMixin, ContextMixin, View):
    login_url = '/account/login/'

    def get(self, request, *args, **kwargs):
        return render(request, 'account/account.html')
