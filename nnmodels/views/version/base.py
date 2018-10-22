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

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from nnmodels.forms import VersionForm
from nnmodels.models import NNModel, Version
from objdetec.decorators import piwik



@method_decorator(piwik('Version • NN Model • N Models • objdetec'),
                  name='dispatch')
class DetailView(generic.DetailView):
    model = Version
    slug_field = 'nnmodel__slug'
    query_pk_and_slug = True

    def get_queryset(self):
        if self.request.user.is_staff:
            return Version.objects.all()
        elif self.request.user.is_authenticated:
            return Version.objects.filter(
                Q(nnmodel__public=True) |
                Q(nnmodel__uploader=self.request.user)
            )
        else:
            return Version.objects.filter(nnmodel__public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_config'] = json.dumps(context['version'].config,
                                             indent=4)
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Create Version • NN Model • NN Models • objdetec'),
                  name='dispatch')
class CreateView(generic.edit.CreateView):
    form_class = VersionForm
    model = Version

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nnmodel'] = self.nnmodel
        return context

    def get_initial(self):
        if self.request.user.is_staff:
            self.nnmodel = NNModel.objects.get(slug=self.kwargs['slug'])
        else:
            self.nnmodel = NNModel.objects. \
                filter(uploader=self.request.user). \
                get(slug=self.kwargs['slug'])
        return {'nnmodel': self.nnmodel}


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Update • Version • NN Model • NN Models • objdetec'),
                  name='dispatch')
class UpdateView(generic.edit.UpdateView):
    form_class = VersionForm
    model = Version
    query_pk_and_slug = True
    slug_field = 'nnmodel__slug'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Version.objects.all()
        else:
            return Version.objects.filter(nnmodel__uploader=self.request.user)
