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

from django.utils import timezone
from objdetec.templatetags.objdetec import register


@register.filter
def startswith(value, start):
    return value.startswith(start)


@register.filter
def endswith(value, end):
    return value.endswith(end)


@register.filter
def get_item(obj, key):
    if type(obj) == list or type(obj) == tuple:
        return obj[key]
    else:
        return obj.get(key)


@register.filter
def as_range(i):
    return range(i)


@register.simple_tag
def timestamp(format_str):
    return timezone.now().strftime(format_str)
