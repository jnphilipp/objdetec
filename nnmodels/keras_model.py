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
import sys

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from utils import Singleton

from .models import NNModel, Version


class KerasModel(metaclass=Singleton):
    def __init__(self):
        self._models = {}

    def get(self, version):
        if version.pk in self._models and \
                type(self._models[version.pk]) is not str:
            return self._models[version.pk]

        path = version.model_file.name
        print(_('Loading model "%(path)s".') % {'path': path})

        try:
            import tensorflow as tf
            from keras import backend as K
            from keras.models import load_model
            with tf.Session(graph=tf.Graph()) as sess:
                K.set_session(sess)
                model = load_model(os.path.join(settings.MEDIA_ROOT, path))
                self._models[version.pk] = model
        except Exception as e:
            print(_('Could not load model.'), e, file=sys.stderr)
            self._models[version.pk] = str(e)
        return self._models[version.pk]

    def get_config(self, version):
        model = self.get(version)
        return {'error': model} if type(model) is str else model.get_config()

    def plot(self, version):
        model = self.get(version)
        if type(model) is str:
            return model
        else:
            img_path = os.path.join(settings.MEDIA_ROOT, version.plot_file())
            img_url = os.path.join(settings.MEDIA_URL, version.plot_file())
            if not os.path.exists(img_path):
                from keras.utils import plot_model
                plot_model(model, to_file=img_path)
            return img_url

    def inputs(self, version):
        model = self.get(version)
        return [model] if type(model) is str else model.inputs

    def outputs(self, version):
        model = self.get(version)
        return [model] if type(model) is str else model.outputs
