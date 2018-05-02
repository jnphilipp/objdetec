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
from django.contrib.auth import authenticate, login, views
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from objdetec.decorators import piwik
from profiles.forms import (AuthenticationForm, PasswordChangeForm,
                            SetPasswordForm, UserCreationForm)


@csrf_protect
@piwik('Sign in • Profile • objdetec')
def signin(request):
    gnext = request.GET.get('next')

    if request.user.is_authenticated:
        print(gnext)
        return redirect(gnext if gnext else 'dashboard')

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

                    return redirect(gnext if gnext else 'dashboard')
                else:
                    messages.add_message(request, messages.ERROR,
                                         _('Your account is disabled.'))
                return redirect(request.META.get('HTTP_REFERER'))
        msg = _('Please enter a correct email and password to sign in. ' +
                'Note that both fields may be case-sensitive.')
        messages.add_message(request, messages.ERROR, msg)
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
@piwik('Sign out • Profile • objdetec')
def signout(request):
    return views.logout(request, template_name='registration/signout.html')


@csrf_protect
@piwik('Password change • Profile • objdetec')
def password_change(request):
    done_url = reverse('profiles:password_change_done')
    return views.password_change(request,
                                 password_change_form=PasswordChangeForm,
                                 post_change_redirect=done_url)


@csrf_protect
@piwik('Password change • Profile • objdetec')
def password_change_done(request):
    return views.password_change_done(request)


@csrf_protect
@piwik('Password reset • Profile • objdetec')
def password_reset(request):
    done_url = reverse('profiles:password_reset_done')
    return views.password_reset(request, post_reset_redirect=done_url)


@csrf_protect
@piwik('Password reset • Profile • objdetec')
def password_reset_done(request):
    return views.password_reset_done(request)


@csrf_protect
@piwik('Password reset • Profile • objdetec')
def password_reset_confirm(request, uidb64=None, token=None):
    complete_url = reverse('profiles:password_reset_complete')
    return views.password_reset_confirm(request, uidb64=uidb64, token=token,
                                        set_password_form=SetPasswordForm,
                                        post_reset_redirect=complete_url)


@csrf_protect
@piwik('Password reset • Profile • objdetec')
def password_reset_complete(request):
    return views.password_reset_complete(request)
