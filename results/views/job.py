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
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from images.models import Image
from nnmodels.models import Version
from objdetec.decorators import piwik

from ..forms import JobForm, JobSetForm
from ..models import Job


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Jobs • Results • objdetec'), name='dispatch')
class ListView(generic.ListView):
    context_object_name = 'jobs'
    model = Job
    paginate_by = 100

    def get_queryset(self):
        jobs = Job.objects.all()
        if not self.request.user.is_staff:
            jobs = jobs.filter(user=self.request.user)
        return jobs


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Job • Results • objdetec'), name='dispatch')
class DetailView(generic.DetailView):
    model = Job

    def get_queryset(self):
        jobs = Job.objects.all()
        if not self.request.user.is_staff:
            jobs = jobs.filter(user=self.request.user)
        return jobs


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Create from image • Job • Results • objdetec'),
                  name='dispatch')
class ImageCreateView(generic.edit.CreateView):
    form_class = JobForm
    model = Job

    def get_form_kwargs(self):
        kwargs = super(ImageCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        return {'version': self.kwargs['version'],
                'image': self.kwargs['image'],
                'user': self.request.user}

    def get_success_url(self):
        from django.urls import reverse
        return reverse('results:job_list')


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Create from set • Job • Results • objdetec'),
                  name='dispatch')
class SetCreateView(generic.edit.CreateView):
    form_class = JobSetForm
    model = Job

    def get_form_kwargs(self):
        kwargs = super(SetCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        return {'version': self.kwargs['version'], 'set': self.kwargs['set'],
                'user': self.request.user}

    def get_success_url(self):
        from django.urls import reverse
        return reverse('results:job_list')
