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

from .models import Job, Output, Result


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'version', 'image', 'state', 'text']}),
        (_('Config'), {'fields': ['overlap']}),
        (_('Result'), {'fields': ['result']}),
    ]
    list_display = ('user', 'version', 'image', 'state')
    list_filter = ('state', 'user', 'version', 'image')
    search_fields = ('user__first_name', 'user__last_name',
                     'version__nnmodel__name', 'version__name', 'image__name')


@admin.register(Output)
class OutputAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name', 't', 'p', 'result']})]
    list_display = ('name', 't', 'result', 'updated_at')
    list_filter = ('t', 'result')
    search_fields = ('name',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['version', 'image']}),
        (_('Config'), {'fields': ['overlap']}),
    ]
    list_display = ('version', 'image', 'updated_at')
    list_filter = ('version', 'image')
    search_fields = ('version__nnmodel__name', 'version__name',
                     'image__name')
