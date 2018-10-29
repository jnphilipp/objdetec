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
from objdetec.decorators import piwik
from nnmodels.models import NNModel

from ..forms import ImageForm
from ..models import Image


@method_decorator(piwik('Images • Images • objdetec'), name='dispatch')
class ListView(generic.ListView):
    context_object_name = 'images'
    model = Image
    paginate_by = 100

    def get_queryset(self):
        if self.request.user.is_staff:
            return Image.objects.all()
        elif self.request.user.is_authenticated:
            return Image.objects.filter(Q(public=True) |
                                        Q(uploader=self.request.user))
        else:
            return Image.objects.filter(public=True)


@method_decorator(piwik('Image • Images • objdetec'), name='dispatch')
class DetailView(generic.DetailView):
    model = Image

    def get_queryset(self):
        if self.request.user.is_staff:
            return Image.objects.all()
        elif self.request.user.is_authenticated:
            return Image.objects.filter(Q(public=True) |
                                        Q(uploader=self.request.user))
        else:
            return Image.objects.filter(public=True)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        if self.request.user.is_staff:
            context['nnmodels'] = NNModel.objects.all()
        elif self.request.user.is_authenticated:
            context['nnmodels'] = NNModel.objects.filter(
                Q(public=True) | Q(uploader=self.request.user))
        else:
            context['nnmodels'] = NNModel.objects.filter(public=True)

        if 'result_id' in self.kwargs:
            context['result'] = context['image'].results.get(
                pk=self.kwargs['result_id'])
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Create Image • Images • objdetec'), name='dispatch')
class CreateView(generic.edit.CreateView):
    model = Image
    form_class = ImageForm

    def get_initial(self):
        return {'uploader': self.request.user}


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Update • Image • Images • objdetec'), name='dispatch')
class UpdateView(generic.edit.UpdateView):
    model = Image
    form_class = ImageForm

    def get_queryset(self):
        if self.request.user.is_staff:
            return Image.objects.all()
        else:
            return Image.objects.filter(uploader=self.request.user)
