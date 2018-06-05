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
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from images.forms import ImageForm
from images.models import Image
from objdetec.decorators import piwik


@piwik('Images • Images • objdetec')
def list(request):
    images = Image.objects.all()
    if request.user.is_authenticated:
        images = images.filter(Q(public=True) | Q(uploader=request.user))
    else:
        images = images.filter(public=True)
    return render(request, 'images/image/list.html', locals())


@piwik('Image • Images • objdetec')
def detail(request, slug):
    image = get_object_or_404(Image, slug=slug)
    if not image.public and request.user != image.uploader:
        msg = _('You are not allowed to access this Image.')
        return HttpResponseForbidden(msg)
    return render(request, 'images/image/detail.html', locals())


@csrf_protect
@login_required
@piwik('Add Image • Images • objdetec')
def add(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            msg = _('Image %(image)s successfully created.')
            messages.add_message(request, messages.SUCCESS,
                                 msg % {'image': image.name})
            return redirect('images:image', slug=image.slug)
    else:
        form = ImageForm(initial={'uploader': request.user})
    return render(request, 'images/image/form.html', locals())


@csrf_protect
@login_required
@piwik('Edit • Image • Images • objdetec')
def edit(request, slug):
    image = get_object_or_404(Image, slug=slug)
    if request.user != image.uploader:
        msg = _('You are not allowed to access this Image.')
        return HttpResponseForbidden(msg)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            image = form.save()
            msg = _('Image %(image)s successfully updated.')
            messages.add_message(request, messages.SUCCESS,
                                 msg % {'image': image.name})
            return redirect('images:image', slug=image.slug)
    else:
        form = ImageForm(instance=image)
    return render(request, 'images/image/form.html', locals())
