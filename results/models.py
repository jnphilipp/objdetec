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

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from objdetec.fields import SingleLineTextField


class Output(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at'))

    name = SingleLineTextField(verbose_name=_('Name'))
    t = models.CharField(max_length=8)
    p = ArrayField(ArrayField(ArrayField(models.FloatField(default=0.))))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Output')
        verbose_name_plural = _('Outputs')


class Result(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at'))

    version = models.ForeignKey('nnmodels.Version', models.CASCADE,
                                related_name='results',
                                verbose_name=_('Version'))
    image = models.ForeignKey('images.Image', models.CASCADE,
                              related_name='results',
                              verbose_name=_('Image'))
    outputs = models.ManyToManyField(Output, related_name='results',
                                     verbose_name=_('Outputs'))

    def __str__(self):
        return '%s - %s' % (self.version, self.image)

    class Meta:
        ordering = ('version', 'image')
        verbose_name = _('Result')
        verbose_name_plural = _('Results')
