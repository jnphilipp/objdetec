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

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
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
