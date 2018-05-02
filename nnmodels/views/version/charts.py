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

from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from nnmodels.models import NNModel, Version
from objdetec.decorators import piwik


@piwik('Train-history chart • Version • NN Model • NN Models • objdetec')
def trainhistory(request, slug, version_id):
    nnmodel = get_object_or_404(NNModel, slug=slug)
    version = get_object_or_404(Version, nnmodel=nnmodel, pk=version_id)

    if not version.trainhistory_file:
        return HttpResponseNotFound('No nn model version has no train-history file.')

    series = []
    with open(version.trainhistory_file.path) as f:
        for k, v in json.loads(f.read()).items():
            series.append({
                'name': k,
                'data': v,
                'yAxis': 0 if 'loss' in k else 1
            })

    return JsonResponse({'series': series})
