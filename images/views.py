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

from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from images.models import Image
from objdetec.decorators import piwik


@piwik('Images • Images • objdetec')
def list(request):
    images = Image.objects.all()
    if request.user.is_authenticated:
        images = images.filter(Q(public=True) | Q(uploader=request.user))
    else:
        images = images.filter(public=True)
    return render(request, 'images/image/list.html', locals())


@piwik('Image • Images • objdetec')
def detail(request, slug):
    image = get_object_or_404(Image, slug=slug)
    if not image.public and request.user != image.uploader:
        msg = _('You are not allowed to access this Image.')
        return HttpResponseForbidden(msg)
    return render(request, 'images/image/detail.html', locals())
