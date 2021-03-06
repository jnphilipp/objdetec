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

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import NNModel, Version


@admin.register(NNModel)
class NNModelAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['slug', 'name', 'description', 'public',
                                    'uploader']})]
    list_display = ('name', 'public', 'uploader')
    list_filter = ('public', 'uploader')
    readonly_fields = ('slug',)
    search_fields = ('name',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nnmodel', 'name', 'model_file',
                           'trainhistory_file']}),
        (_('FSM state'), {'fields': ['state']}),
        (_('Model values'), {'fields': ['inputs', 'outputs', 'config',
                                        'nb_trainable', 'nb_non_trainable']})
    ]
    list_display = ('nnmodel', 'name', 'state', 'updated_at')
    list_filter = ('nnmodel', 'state')
    search_fields = ('nnmodel__name', 'name')
