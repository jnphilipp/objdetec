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

from .models import NNModel, Version


class NNModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NNModelForm, self).__init__(*args, **kwargs)
        self.fields['uploader'].widget = forms.HiddenInput()

    def clean_name(self):
        return self.cleaned_data['name'] or None

    class Meta:
        model = NNModel
        fields = ('name', 'description', 'public', 'uploader')


class VersionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        self.fields['nnmodel'].widget = forms.HiddenInput()

    def clean_name(self):
        return self.cleaned_data['name'] or None

    class Meta:
        model = Version
        fields = ('nnmodel', 'name', 'model_file', 'trainhistory_file')
