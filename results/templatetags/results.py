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

import base64
import numpy as np
import os

from django.template import Library
from io import BytesIO
from keras.preprocessing import image
from PIL import Image

register = Library()


@register.filter
def array_to_img(array, c=None):
    rgb = np.zeros((len(array), len(array[0]), 3))
    for i in range(len(array)):
        for j in range(len(array[0])):
                if c is None:
                    rgb[i, j, :] = array[i][j]
                else:
                    rgb[i, j, :] = array[i][j][c]
    img = image.array_to_img(rgb)
    buffer = BytesIO()
    img.save(buffer, 'png')
    b = b'data:image/png;base64,%s' % base64.b64encode(buffer.getvalue())
    return b.decode('utf-8')


@register.filter
def nb_classes(output):
    if output.t == 'class':
        return len(output.p[0][0])
    else:
        return 0
