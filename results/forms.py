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

from django import forms
from django.utils.translation import ugettext_lazy as _
from images.models import Image, Set
from nnmodels.models import Version

from .models import Job


class JobForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()

        if user.is_staff:
            self.fields['image'].queryset = Image.objects.all()
            self.fields['version'].queryset = Version.objects.all()
        elif user.is_authenticated:
            self.fields['image'].queryset = Image.objects.filter(
                Q(public=True) | Q(uploader=user))
            self.fields['version'].queryset = Version.objects.filter(
                Q(nnmodel__public=True) | Q(nnmodel__uploader=user))
        else:
            self.fields['image'].queryset = Image.objects.filter(public=True)
            self.fields['version'].queryset = Version.objects.filter(
                nnmodel__public=True)

        self.fields['image'].widget.attrs['style'] = 'width: 100%;'
        self.fields['version'].widget.attrs['style'] = 'width: 100%;'

    class Meta:
        model = Job
        fields = ('version', 'image', 'overlap', 'user')


class JobSetForm(forms.ModelForm):
    set = forms.ModelChoiceField(Set.objects.all())

    def __init__(self, user, *args, **kwargs):
        super(JobSetForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()

        if user.is_staff:
            self.fields['set'].queryset = Set.objects.all()
            self.fields['version'].queryset = Version.objects.all()
        elif user.is_authenticated:
            self.fields['set'].queryset = Set.objects.filter(Q(public=True) |
                                                             Q(uploader=user))
            self.fields['version'].queryset = Version.objects.filter(
                Q(nnmodel__public=True) | Q(nnmodel__uploader=user))
        else:
            self.fields['set'].queryset = Set.objects.filter(public=True)
            self.fields['version'].queryset = Version.objects.filter(
                nnmodel__public=True)

        self.fields['set'].widget.attrs['style'] = 'width: 100%;'
        self.fields['version'].widget.attrs['style'] = 'width: 100%;'

    def save(self, commit=True, *args, **kwargs):
        self.jobs = []

        if self.cleaned_data['user'].is_staff:
            images = self.cleaned_data['set'].images.all()
        elif self.cleaned_data['user'].is_authenticated:
            images = self.cleaned_data['set'].images.filter(
                Q(public=True) | Q(uploader=self.cleaned_data['user']))
        else:
            images = self.cleaned_data['set'].images.filter(public=True)

        for image in images:
            self.jobs.append(Job(overlap=self.instance.overlap,
                                 version=self.instance.version,
                                 user=self.instance.user, image=image))

        if commit:
            for job in self.jobs:
                job.save()

        self.instance = self.jobs[0]
        return self.instance

    class Meta:
        model = Job
        fields = ('version', 'set', 'overlap', 'user')
