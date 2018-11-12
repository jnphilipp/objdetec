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

import numpy as np
import os

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.files import File
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField, transition
from keras.preprocessing import image
from nnmodels.keras_model import predict_image
from objdetec.fields import SingleLineTextField
from PIL import Image
from tempfile import NamedTemporaryFile

from .validators import validate_prob


def get_image_path(instance, filename):
    name = slugify(instance.name) + '.png'
    if instance.result.image.set:
        return os.path.join('images', slugify(instance.result.image.set.name),
                            slugify(instance.result.image.name), 'results',
                            str(instance.result.pk), name)
    return os.path.join('images', slugify(instance.result.image.name),
                        'results', str(instance.result.pk), name)


class Result(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at'))

    version = models.ForeignKey('nnmodels.Version', models.CASCADE,
                                related_name='results',
                                verbose_name=_('Version'))
    image = models.ForeignKey('images.Image', models.CASCADE,
                              related_name='results', verbose_name=_('Image'))
    overlap = models.FloatField(default=0.75, validators=[validate_prob],
                                verbose_name=_('Overlap'))

    def __str__(self):
        return '%s - %s' % (self.version, self.image)

    class Meta:
        ordering = ('version', 'image')
        verbose_name = _('Result')
        verbose_name_plural = _('Results')


class Output(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at'))

    name = SingleLineTextField(verbose_name=_('Name'))
    t = models.CharField(max_length=8)
    p = models.ImageField(upload_to=get_image_path, max_length=4096)
    result = models.ForeignKey(Result, models.CASCADE, related_name='outputs',
                               verbose_name=_('Result'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Output')
        verbose_name_plural = _('Outputs')


class Job(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at'))

    state = FSMField(default='new', verbose_name=_('State'))
    text = models.TextField(blank=True, null=True, verbose_name=_('Text'))
    overlap = models.FloatField(default=0.75, validators=[validate_prob],
                                verbose_name=_('Overlap'))
    version = models.ForeignKey('nnmodels.Version', models.CASCADE,
                                related_name='jobs', verbose_name=_('Version'))
    result = models.OneToOneField(Result, models.CASCADE, blank=True,
                                  null=True, related_name='job',
                                  verbose_name=_('Result'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                             related_name='jobs', verbose_name=_('User'))
    image = models.ForeignKey('images.Image', models.CASCADE,
                              related_name='jobs', verbose_name=_('Image'))

    def get_absolute_url(self):
        return reverse('results:job_detail', args=[self.pk])

    @transition(field=state, source=('new', 'failed'), target='predicted',
                on_error='failed')
    def predict(self, batch_size, data_format):
        def create_output(img, name, result):
            with NamedTemporaryFile(mode='bw+') as f:
                img.save(f, format='png')
                output = Output(name=name, result=result, t=outputs[i]['t'])
                output.p.save('%s.png' % name, File(open(f.name, 'rb')))
                output.save()

        assert data_format in ('channels_first', 'channels_last')

        path = os.path.join(settings.MEDIA_ROOT, self.image.image.path)
        history, outputs = predict_image(self.version, path,
                                         batch_size=batch_size,
                                         overlap=self.overlap,
                                         data_format=data_format)

        result = Result.objects.create(version=self.version,
                                       image=self.image,
                                       overlap=self.overlap)

        for i in range(len(outputs)):
            if outputs[i]['t'] == 'class':
                if data_format == 'channels_first':
                    nb_classes = outputs[i]['img'].shape[0]
                elif data_format == 'channels_last':
                    nb_classes = outputs[i]['img'].shape[2]

                for j in range(nb_classes):
                    if data_format == 'channels_first':
                        p = outputs[i]['img'][j, :, :]
                        p = np.repeat(p.reshape((1,) + p.shape), 3, axis=0)
                    elif data_format == 'channels_last':
                        p = outputs[i]['img'][:, :, j]
                        p = np.repeat(p.reshape(p.shape + (1,)), 3, axis=2)

                    name = '%s:%s' % (outputs[i]['name'], j)
                    create_output(array_to_img(p), name, result)
            elif outputs[i]['t'] == 'img':
                create_output(array_to_img(outputs[i]['img']),
                              outputs[i]['name'], result)
        self.result = result

    def __str__(self):
        return '%s [%s - %s]' % (self.user, self.version, self.image)

    class Meta:
        ordering = ('user', 'version', 'image')
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')
