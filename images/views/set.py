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
from django.db import transaction
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import generic
from nnmodels.models import NNModel
from objdetec.decorators import piwik
from results.models import Result

from ..forms import ImageFormSet, SetForm
from ..models import Set


@method_decorator(piwik('Set • Images • objdetec'), name='dispatch')
class DetailView(generic.DetailView):
    model = Set

    def get_queryset(self):
        if self.request.user.is_staff:
            return Set.objects.all()
        elif self.request.user.is_authenticated:
            return Set.objects.filter(Q(public=True) |
                                      Q(uploader=self.request.user))
        else:
            return Set.objects.filter(public=True)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        if self.request.user.is_staff:
            context['images'] = context['set'].images.all()
            context['nnmodels'] = NNModel.objects.all()
        elif self.request.user.is_authenticated:
            context['images'] = context['set'].images.filter(
                Q(public=True) | Q(uploader=self.request.user))
            context['nnmodels'] = NNModel.objects.filter(
                Q(public=True) | Q(uploader=self.request.user))
        else:
            context['images'] = context['set'].images.filter(public=True)
            context['nnmodels'] = NNModel.objects.filter(public=True)

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Set • Images • objdetec'), name='dispatch')
class CreateView(generic.CreateView):
    form_class = SetForm
    model = Set

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST,
                                                    self.request.FILES)
        else:
            context['image_formset'] = ImageFormSet()
        return context

    def get_initial(self):
        return {'uploader': self.request.user}

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        with transaction.atomic():
            if image_formset.is_valid():
                self.object = form.save()

                images = image_formset.save(commit=False)
                for image in images:
                    image.set = self.object
                    image.uploader = self.request.user
                    image.save()
                return super(CreateView, self).form_valid(form)
            else:
                return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Update • Set • Images • objdetec'), name='dispatch')
class UpdateView(generic.UpdateView):
    form_class = SetForm
    model = Set

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST,
                                                    self.request.FILES)
        else:
            context['image_formset'] = ImageFormSet()
        return context

    def get_initial(self):
        return {'uploader': self.request.user}

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        with transaction.atomic():
            if image_formset.is_valid():
                self.object = form.save()

                images = image_formset.save(commit=False)
                for image in images:
                    image.set = self.object
                    image.uploader = self.request.user
                    image.save()
                return super(UpdateView, self).form_valid(form)
            else:
                return self.form_invalid(form)
