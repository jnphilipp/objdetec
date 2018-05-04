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
from nnmodels.forms import NNModelForm
from nnmodels.models import NNModel
from objdetec.decorators import piwik


@piwik('NN Models • NN Models • objdetec')
def list(request):
    nnmodels = NNModel.objects.all()
    if request.user.is_authenticated:
        nnmodels = nnmodels.filter(Q(public=True) | Q(uploader=request.user))
    else:
        nnmodels = nnmodels.filter(public=True)
    return render(request, 'nnmodels/nnmodel/list.html', locals())


@piwik('NN Model • NN Models • objdetec')
def detail(request, slug):
    nnmodel = get_object_or_404(NNModel, slug=slug)
    if not nnmodel.public and request.user != nnmodel.uploader:
        msg = _('You are not allowed to access this NNModel.')
        return HttpResponseForbidden(msg)
    return render(request, 'nnmodels/nnmodel/detail.html', locals())


@csrf_protect
@login_required
@piwik('Add NN Model • NN Models • objdetec')
def add(request):
    if request.method == 'POST':
        form = NNModelForm(request.POST)
        if form.is_valid():
            nnmodel = form.save()
            msg = _('NNModel "%(name)s" successfully created.')
            messages.add_message(request, messages.SUCCESS,
                                 msg % {'name': nnmodel.name})
            return redirect('nnmodels:nnmodel', slug=nnmodel.slug)
    else:
        form = NNModelForm(initial={'uploader': request.user})
    return render(request, 'nnmodels/nnmodel/form.html', locals())


@csrf_protect
@login_required
@piwik('Edit • NN Model • NN Models • objdetec')
def edit(request, slug):
    nnmodel = get_object_or_404(NNModel, slug=slug)
    if request.user != nnmodel.uploader:
        msg = _('You are not allowed to access this NNModel.')
        return HttpResponseForbidden(msg)

    if request.method == 'POST':
        form = NNModelForm(request.POST, instance=nnmodel)
        if form.is_valid():
            nnmodel = form.save()
            msg = _('NNModel "%(name)s" successfully updated.')
            messages.add_message(request, messages.SUCCESS,
                                 msg % {'name': nnmodel.name})
            return redirect('nnmodels:nnmodel', slug=nnmodel.slug)
    else:
        form = NNModelForm(instance=nnmodel)
    return render(request, 'nnmodels/nnmodel/form.html', locals())
