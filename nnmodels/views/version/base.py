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

import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from nnmodels.forms import VersionForm
from nnmodels.keras_model import KerasModel
from nnmodels.models import NNModel, Version
from objdetec.decorators import piwik


@piwik('Version • NN Model • NN Models • objdetec')
def detail(request, slug, version_id):
    nnmodel = get_object_or_404(NNModel, slug=slug)
    version = get_object_or_404(Version, nnmodel=nnmodel, pk=version_id)
    if not nnmodel.public and request.user != nnmodel.uploader:
        msg = _('You are not allowed to access this NNModel.')
        return HttpResponseForbidden(msg)
    return render(request, 'nnmodels/version/detail.html', locals())


@piwik('Config • Version • NN Model • NN Models • objdetec')
def config(request, slug, version_id):
    nnmodel = get_object_or_404(NNModel, slug=slug)
    version = get_object_or_404(Version, nnmodel=nnmodel, pk=version_id)
    model_config = json.dumps(KerasModel().get_config(version), indent=4)
    if not nnmodel.public and request.user != nnmodel.uploader:
        msg = _('You are not allowed to access this NNModel.')
        return HttpResponseForbidden(msg)
    return render(request, 'nnmodels/version/config.html', locals())


@piwik('Plot • Version • NN Model • NN Models • objdetec')
def plot(request, slug, version_id):
    nnmodel = get_object_or_404(NNModel, slug=slug)
    version = get_object_or_404(Version, nnmodel=nnmodel, pk=version_id)
    plot_url = KerasModel().plot(version)
    if not nnmodel.public and request.user != nnmodel.uploader:
        msg = _('You are not allowed to access this NNModel.')
        return HttpResponseForbidden(msg)
    return render(request, 'nnmodels/version/plot.html', locals())


@csrf_protect
@login_required
@piwik('Add Version • NN Model • NN Models • objdetec')
def add(request, slug):
    nnmodel = get_object_or_404(NNModel, slug=slug)
    if request.user != nnmodel.uploader:
        msg = _('You are not allowed to access this NNModel.')
        return HttpResponseForbidden(msg)

    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES)
        if form.is_valid():
            version = form.save()
            msg = _('Version %(version)s for NNModel "%(nnmodel)s" '
                    'successfully created.')
            messages.add_message(request, messages.SUCCESS,
                                 msg % {'version': version.name,
                                        'nnmodel': nnmodel.name})
            return redirect('nnmodels:version', slug=nnmodel.slug,
                            version_id=version.pk)
    else:
        form = VersionForm(initial={'nnmodel': nnmodel})
    return render(request, 'nnmodels/version/form.html', locals())


@csrf_protect
@login_required
@piwik('Edit • Version • NN Model • NN Models • objdetec')
def edit(request, slug, version_id):
    nnmodel = get_object_or_404(NNModel, slug=slug)
    version = get_object_or_404(Version, nnmodel=nnmodel, pk=version_id)
    if request.user != nnmodel.uploader:
        msg = _('You are not allowed to access this NNModel.')
        return HttpResponseForbidden(msg)

    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES, instance=version)
        if form.is_valid():
            version = form.save()
            msg = _('Version %(version)s for NNModel "%(nnmodel)s" '
                    'successfully updated.')
            messages.add_message(request, messages.SUCCESS,
                                 msg % {'version': version.name,
                                        'nnmodel': nnmodel.name})
            return redirect('nnmodels:version', slug=nnmodel.slug,
                            version_id=version.pk)
    else:
        form = VersionForm(instance=version)
    return render(request, 'nnmodels/version/form.html', locals())
