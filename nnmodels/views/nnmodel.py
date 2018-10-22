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

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import generic
from nnmodels.forms import NNModelForm
from nnmodels.models import NNModel
from objdetec.decorators import piwik


@method_decorator(piwik('NN Models • NN Models • objdetec'), name='dispatch')
class ListView(generic.ListView):
    context_object_name = 'nnmodels'
    model = NNModel
    paginate_by = 100

    def get_queryset(self):
        if self.request.user.is_staff:
            return NNModel.objects.all()
        elif self.request.user.is_authenticated:
            return NNModel.objects.filter(Q(public=True) |
                                          Q(uploader=self.request.user))
        else:
            return NNModel.objects.filter(public=True)


@method_decorator(piwik('NN Models • NN Models • objdetec'), name='dispatch')
class DetailView(generic.DetailView):
    model = NNModel

    def get_queryset(self):
        if self.request.user.is_staff:
            return NNModel.objects.all()
        elif self.request.user.is_authenticated:
            return NNModel.objects.filter(Q(public=True) |
                                          Q(uploader=self.request.user))
        else:
            return NNModel.objects.filter(public=True)


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Create NN Model • NN Models • objdetec'),
                  name='dispatch')
class CreateView(generic.edit.CreateView):
    model = NNModel
    form_class = NNModelForm

    def get_initial(self):
        return {'uploader': self.request.user}


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Update • NN Model • NN Models • objdetec'),
                  name='dispatch')
class UpdateView(generic.edit.UpdateView):
    model = NNModel
    form_class = NNModelForm

    def get_queryset(self):
        if self.request.user.is_staff:
            return NNModel.objects.all()
        else:
            return NNModel.objects.filter(uploader=self.request.user)
