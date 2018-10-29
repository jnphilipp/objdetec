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

from .models import Image, Set


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['slug', 'name', 'public', 'image',
                                    'uploader', 'set']})]
    list_display = ('name', 'public', 'uploader', 'set')
    list_filter = ('public', 'uploader', 'set')
    readonly_fields = ('slug',)
    search_fields = ('name',)


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['slug', 'name', 'public', 'uploader']})]
    list_display = ('name', 'public', 'uploader')
    list_filter = ('public', 'uploader')
    readonly_fields = ('slug',)
    search_fields = ('name',)
