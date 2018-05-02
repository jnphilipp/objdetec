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

from django.db.models import Q
from django.shortcuts import get_object_or_404, render
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
    return render(request, 'nnmodels/nnmodel/detail.html', locals())
