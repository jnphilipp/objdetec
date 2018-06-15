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

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from objdetec.fields import SingleLineTextField


def get_file_path(instance, filename):
    return os.path.join('nnmodels', str(instance.nnmodel.slug),
                        slugify(instance.name), filename)


class NNModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at'))

    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    name = SingleLineTextField(unique=True, verbose_name=_('Name'))
    description = models.TextField(blank=True, null=True,
                                   verbose_name=_('Description'))
    public = models.BooleanField(default=True, verbose_name=_('Public'))
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                                 related_name='nnmodels',
                                 verbose_name=_('Uploader'))

    def get_absolute_url(self):
        return reverse('nnmodels:nnmodel', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            orig = NNModel.objects.get(pk=self.pk)
            if orig.name != self.name:
                self.slug = slugify(self.name)
        super(NNModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('NN Model')
        verbose_name_plural = _('NN Models')


class Version(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at'))

    nnmodel = models.ForeignKey(NNModel, models.CASCADE,
                                related_name='versions',
                                verbose_name=_('NN Model'))
    name = SingleLineTextField(verbose_name=_('Name'))
    model_file = models.FileField(upload_to=get_file_path,
                                  max_length=4096,
                                  verbose_name=_('Model file'))
    trainhistory_file = models.FileField(upload_to=get_file_path, blank=True,
                                         null=True, max_length=4096,
                                         verbose_name=_('Train-history file'))

    def plot_file(self):
        return '%s.png' % self.model_file

    def save(self, *args, **kwargs):
        if self.pk:
            orig = Version.objects.get(pk=self.pk)
            if orig.model_file != self.model_file:
                path = os.path.join(settings.MEDIA_ROOT, orig.plot_file())
                if os.path.exists(path):
                    os.remove(path)

                path = os.path.join(settings.MEDIA_ROOT,
                                    orig.model_file.name)
                if os.path.exists(path):
                    os.remove(path)
            if orig.trainhistory_file and \
                    orig.trainhistory_file != self.trainhistory_file:
                path = os.path.join(settings.MEDIA_ROOT,
                                    orig.trainhistory_file.name)
                if os.path.exists(path):
                    os.remove(path)
        super(Version, self).save(*args, **kwargs)

    def __str__(self):
        return '%s [%s]' % (self.nnmodel, self.name)

    class Meta:
        ordering = ('nnmodel', '-updated_at')
        unique_together = ('nnmodel', 'name')
        verbose_name = _('Version')
        verbose_name_plural = _('Versions')
