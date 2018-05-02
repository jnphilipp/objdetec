# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from objdetec.decorators import piwik
from profiles.forms import UserChangeForm


@csrf_protect
@login_required
@piwik('Profile • objdetec')
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,
                             _('Your profile has been successfully updated.'))
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'profiles/profile_detail.html', locals())
