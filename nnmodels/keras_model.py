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

import math
import numpy as np
import os
import time

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from keras import backend as K
from keras.callbacks import BaseLogger, CallbackList, History, ProgbarLogger
from keras.preprocessing.image import img_to_array, load_img
from keras.models import load_model


def predict_image(version, image_path, batch_size, overlap, data_format=None):
    def current_time_millis():
        return int(round(time.time() * 1000))

    def offset(size, diff, overlap):
        return math.floor(diff / math.ceil(diff / (size * (1 - overlap))))

    def map_c(i, j, b, l):
        return int(((i * b) + j) / l)

    def map_r(i, j, b, l):
        return ((i * b) + j) % l

    if data_format is None:
        data_format = K.image_data_format()
    if data_format not in {'channels_first', 'channels_last'}:
        raise ValueError('Unknown data_format:', data_format)

    path = version.model_file.name
    print(_('Loading model "%(path)s".') % {'path': path})
    model = load_model(os.path.join(settings.MEDIA_ROOT, path))

    if len(model.inputs) != 1:
        raise RuntimeError('Models with more than one input are not'
                           ' supported at the moment.')

    inputs = []
    for i in range(len(model.inputs)):
        name = model.inputs[i].name
        pos = min(name.index('/') if '/' in name else len(name),
                  name.index(':') if ':' in name else len(name))
        name = name[:pos]

        inputs.append({
            'shape': model.inputs[i].shape.as_list(),
            'name': name
        })
        if data_format == 'channels_first':
            inputs[i]['grayscale'] = inputs[i]['shape'][1] == 1
            inputs[i]['r'] = inputs[i]['shape'][2]
            inputs[i]['c'] = inputs[i]['shape'][3]
        elif data_format == 'channels_last':
            inputs[i]['r'] = inputs[i]['shape'][1]
            inputs[i]['c'] = inputs[i]['shape'][2]
            inputs[i]['grayscale'] = inputs[i]['shape'][3] == 1

        inputs[i]['img'] = img_to_array(load_img(image_path,
                                                 inputs[i]['grayscale']))
        inputs[i]['img'] *= 1./255
        if data_format == 'channels_first':
            inputs[i]['img_r'] = inputs[i]['img'].shape[1]
            inputs[i]['img_c'] = inputs[i]['img'].shape[2]
        elif data_format == 'channels_last':
            inputs[i]['img_r'] = inputs[i]['img'].shape[0]
            inputs[i]['img_c'] = inputs[i]['img'].shape[1]

        inputs[i]['diff_r'] = inputs[i]['img_r'] - inputs[i]['r']
        inputs[i]['diff_c'] = inputs[i]['img_c'] - inputs[i]['c']
        inputs[i]['offset_r'] = offset(inputs[i]['r'], inputs[i]['diff_r'],
                                       overlap)
        inputs[i]['offset_c'] = offset(inputs[i]['c'], inputs[i]['diff_c'],
                                       overlap)
        inputs[i]['nb_r'] = math.ceil(inputs[i]['diff_r'] /
                                      inputs[i]['offset_r']) + 1
        inputs[i]['nb_c'] = math.ceil(inputs[i]['diff_c'] /
                                      inputs[i]['offset_c']) + 1
    inputs = inputs[0]
    N = inputs['nb_r'] * inputs['nb_c']
    steps = math.ceil(N / batch_size)

    metrics = []
    outputs = []
    for i in range(len(model.outputs)):
        tshape = model.outputs[i].shape.as_list()
        name = model.outputs[i].name
        pos = min(name.index('/') if '/' in name else len(name),
                  name.index(':') if ':' in name else len(name))
        name = name[:pos]
        activation = model.get_layer(name).activation.__name__.lower()
        outputs.append({'name': name, 'shape': tshape})

        if len(tshape) == 2:
            if activation == 'softmax':
                outputs[i]['t'] = 'class'
            else:
                outputs[i]['t'] = 'multi'

            nb_classes = tshape[1]
            if nb_classes is None:
                nb_classes = model.get_layer(name).output_shape[1]
            nb_classes = int(nb_classes)
            metrics += ['%s:%s' % (name, i) for i in range(nb_classes)]

            if data_format == 'channels_first':
                shape = (nb_classes, inputs['nb_r'], inputs['nb_c'])
            elif data_format == 'channels_last':
                shape = (inputs['nb_r'], inputs['nb_c'], nb_classes)

        elif len(tshape) == 4:
            if activation == 'softmax':
                outputs[i]['t'] = 'class'
            else:
                outputs[i]['t'] = 'img'

            shape = (inputs['nb_r'], inputs['nb_c']) + tuple(tshape[1:])
        outputs[i]['p'] = np.zeros(shape)

    history = History()
    callbacks = CallbackList([BaseLogger(), history, ProgbarLogger()])
    callbacks.set_model(model)
    callbacks.set_params({
        'batch_size': batch_size,
        'epochs': 1,
        'steps': steps,
        'samples': N,
        'verbose': 1,
        'do_validation': False,
        'metrics': metrics,
    })

    callbacks.on_train_begin()
    callbacks.on_epoch_begin(0)
    start_time = current_time_millis()
    for b in range(steps):
        current_index = (b * batch_size) % N
        if N >= current_index + batch_size:
            current_batch_size = batch_size
        else:
            current_batch_size = N - current_index

        batch_logs = {'batch': b, 'size': current_batch_size}
        for metric in metrics:
            batch_logs[metric] = 0
        callbacks.on_batch_begin(b, batch_logs)

        bX = np.zeros((current_batch_size,) + tuple(inputs['shape'][1:]))
        for j in range(current_batch_size):
            idx_r = map_r(b, j, batch_size, inputs['nb_r'])
            idx_c = map_c(b, j, batch_size, inputs['nb_r'])
            top = min(idx_r * inputs['offset_r'],
                      inputs['img_r'] - inputs['r'])
            bottom = min(idx_r * inputs['offset_r'] + inputs['r'],
                         inputs['img_r'])
            left = min(idx_c * inputs['offset_c'],
                       inputs['img_c'] - inputs['c'])
            right = min(idx_c * inputs['offset_c'] + inputs['c'],
                        inputs['img_c'])

            if data_format == 'channels_first':
                bX[j] = inputs['img'][:, top:bottom, left:right]
            elif data_format == 'channels_last':
                bX[j] = inputs['img'][top:bottom, left:right, :]

        p = model.predict_on_batch(bX)
        if type(p) != list:
            p = [p]
        for j in range(current_batch_size):
            for i in range(len(outputs)):
                idx_r = map_r(b, j, batch_size, inputs['nb_r'])
                idx_c = map_c(b, j, batch_size, inputs['nb_r'])

                if len(outputs[i]['p'].shape) == 3:
                    if data_format == 'channels_first':
                        outputs[i]['p'][:, idx_r, idx_c] = p[i][j]
                    elif data_format == 'channels_last':
                        outputs[i]['p'][idx_r, idx_c, :] = p[i][j]
                    metric = metrics[p[i][j].argmax()]
                    batch_logs[metric] += 1. / current_batch_size
                elif len(outputs[i]['p'].shape) == 5:
                    outputs[i]['p'][idx_r, idx_c, :, :, :] = p[i][j]
        callbacks.on_batch_end(b, batch_logs)
    runtime = (current_time_millis() - start_time) / 1000
    callbacks.on_epoch_end(0, {'runtime': runtime})
    callbacks.on_train_end()

    for i in range(len(outputs)):
        if len(outputs[i]['shape']) == 2:
            if data_format == 'channels_first':
                shape = (outputs[i]['p'].shape[0], inputs['img_r'],
                         inputs['img_c'])
            elif data_format == 'channels_last':
                shape = (inputs['img_r'], inputs['img_c'],
                         outputs[i]['p'].shape[2])
        elif len(tshape) == 4:
            if data_format == 'channels_first':
                shape = (outputs[i]['p'].shape[2], inputs['img_r'],
                         inputs['img_c'])
            elif data_format == 'channels_last':
                shape = (inputs['img_r'], inputs['img_c'],
                         outputs[i]['p'].shape[4])

        count = np.zeros(shape)
        outputs[i]['img'] = np.zeros(shape)
        if len(outputs[i]['p'].shape) == 3:
            if data_format == 'channels_first':
                nb_rows = outputs[i]['p'].shape[1]
                nb_cols = outputs[i]['p'].shape[2]
            elif data_format == 'channels_last':
                nb_rows = outputs[i]['p'].shape[0]
                nb_cols = outputs[i]['p'].shape[1]
        elif len(outputs[i]['p'].shape) == 5:
            nb_rows = outputs[i]['p'].shape[0]
            nb_cols = outputs[i]['p'].shape[1]

        for j in range(nb_rows):
            for k in range(nb_cols):
                top = min(j * inputs['offset_r'],
                          inputs['img_r'] - inputs['r'])
                bottom = min(j * inputs['offset_r'] + inputs['r'],
                             inputs['img_r'])
                left = min(k * inputs['offset_c'],
                           inputs['img_c'] - inputs['c'])
                right = min(k * inputs['offset_c'] + inputs['c'],
                            inputs['img_c'])

                if data_format == 'channels_first':
                    outputs[i]['img'][:, top:bottom, left:right] += \
                        outputs[i]['p'][:, j, k]
                    count[:, top:bottom, left:right] += 1
                elif data_format == 'channels_last':
                    outputs[i]['img'][top:bottom, left:right, :] += \
                        outputs[i]['p'][j, k, :]
                    count[top:bottom, left:right, :] += 1
        outputs[i]['img'] /= count
        del outputs[i]['p']
        del outputs[i]['shape']
    return history.history, outputs
