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

from django.template import Library

register = Library()


@register.filter
def basename(path):
    return os.path.basename(path if type(path) == str else str(path))


@register.filter
def total_params(version):
    if version.nb_trainable is None and version.nb_non_trainable is None:
        return None
    elif version.nb_trainable is not None and version.nb_non_trainable is None:
        return version.nb_trainable
    elif version.nb_trainable is None and version.nb_non_trainable is not None:
        return version.nb_non_trainable
    else:
        return version.nb_trainable + version.nb_non_trainable
