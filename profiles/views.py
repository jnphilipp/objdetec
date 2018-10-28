# -*- coding: utf-8 -*-
# Copyright (C) 2018 Nathanael Philipp (jnphilipp) <mail@jnphilipp.org>
#
# This file is part of objdetec.
#
# objdetec is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# objdetec is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with objdetec.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from objdetec.decorators import piwik

from .forms import AuthenticationForm, UserChangeForm, UserCreationForm
from .models import User


@csrf_protect
@piwik('Sign in • Profile • objdetec')
def signin(request):
    gnext = request.GET.get('next')

    if request.user.is_authenticated:
        return redirect(gnext) if gnext else redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS,
                                         _('You have successfully signed in.'))

                    return redirect(gnext) if gnext else redirect('dashboard')
                else:
                    messages.add_message(request, messages.ERROR,
                                         _('Your account is disabled.'))
                return redirect(request.META.get('HTTP_REFERER'))
        messages.add_message(request, messages.ERROR,
                             _('Please enter a correct email and password to' +
                               ' sign in. Note that both fields may be ' +
                               'case-sensitive.'))
    else:
        form = AuthenticationForm(request)
    return render(request, 'registration/signin.html', locals())


@csrf_protect
@piwik('Sign up • Profile • objdetec')
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, messages.SUCCESS,
                          _('Thanks for signing up. You are now logged in.'))
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('profiles:profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', locals())


@csrf_protect
@login_required
@piwik('Profile • objdetec')
def profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = UserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,
                             _('Your profile has been successfully updated.'))
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'profiles/profile_detail.html', locals())


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Profile • objdetec'), name='dispatch')
class UpdateView(generic.edit.UpdateView):
    model = User
    form_class = UserChangeForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        from django.urls import reverse
        return reverse('profiles:profile')
