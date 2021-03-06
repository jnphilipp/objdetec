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

import os

from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .models import Image, Set


class ImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['set'].widget.attrs['style'] = 'width: 100%;'
        self.fields['uploader'].widget = forms.HiddenInput()

    def clean_name(self):
        return self.cleaned_data['name'] or None

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['name'] is None:
            cleaned_data['name'] = os.path.splitext(
                str(cleaned_data['image']))[0]
        return cleaned_data

    class Meta:
        model = Image
        fields = ('name', 'public', 'image', 'uploader', 'set')


class ImageInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageInlineForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False

    def clean_name(self):
        return self.cleaned_data['name'] or None

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['name'] is None:
            cleaned_data['name'] = os.path.splitext(
                str(cleaned_data['image']))[0]
        return cleaned_data

    class Meta:
        model = Image
        fields = ('name', 'public', 'image')


class SetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SetForm, self).__init__(*args, **kwargs)
        self.fields['uploader'].widget = forms.HiddenInput()

    def clean_name(self):
        return self.cleaned_data['name'] or None

    class Meta:
        model = Set
        fields = ('name', 'public', 'uploader')


ImageFormSet = forms.inlineformset_factory(Set, Image, ImageInlineForm,
                                           extra=1)
