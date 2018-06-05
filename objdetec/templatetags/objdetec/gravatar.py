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

import hashlib
import urllib

from objdetec.templatetags.objdetec import register
from django.utils.safestring import mark_safe


@register.simple_tag(takes_context=True)
def gravatar(context, size=40, default='identicon'):
    if context['user'].is_authenticated:
        email = context['user'].email.lower().encode('utf-8')
    else:
        email = ''.encode('utf-8')

    return 'https://www.gravatar.com/avatar/%s?%s' % (
        hashlib.md5(email).hexdigest(),
        urllib.parse.urlencode({'s': str(size), 'd': default})
    )


@register.simple_tag(takes_context=True)
def gravatar_img(context, size=40, default='identicon', classes=''):
    img_str = '<img class="%s" src="%s" height="%d" width="%d">'
    return mark_safe(img_str % (classes, gravatar(context, size, default),
                                size, size))
