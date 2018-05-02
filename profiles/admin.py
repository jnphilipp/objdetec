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
from django.contrib.auth import admin as auth_admin
from django.utils.translation import ugettext_lazy as _

from .forms import UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    add_fieldsets = (
        (None, {'fields': ('email', 'first_name', 'password1', 'password2')}),
    )
    add_form = UserCreationForm
    exclude = ('username',)
    fieldsets = auth_admin.UserAdmin.fieldsets
    fieldsets[0][1]['fields'] = ('email', 'password', 'unique_visitor_id')
    fieldsets[1][1]['fields'] = ('first_name', 'last_name')
    list_display = ('email', 'first_name', 'last_name', 'is_active',
                    'is_staff')
    ordering = ('email',)
    readonly_fields = ('unique_visitor_id',)
    search_fields = ('email', 'first_name', 'last_name', 'unique_visitor_id')
