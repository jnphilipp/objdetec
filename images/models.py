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
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from objdetec.fields import SingleLineTextField


def get_image_path(instance, filename):
    name = slugify(instance.name) + os.path.splitext(filename)[1]
    if instance.set:
        return os.path.join('images', slugify(instance.set.name),
                            slugify(instance.name), name)
    return os.path.join('images', slugify(instance.name), name)


class Set(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at'))

    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    name = SingleLineTextField(unique=True, verbose_name=_('Name'))
    public = models.BooleanField(default=True, verbose_name=_('Public'))
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                                 related_name='sets',
                                 verbose_name=_('Uploader'))

    def get_absolute_url(self):
        return reverse('images:set_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            orig = Set.objects.get(pk=self.pk)
            if orig.name != self.name:
                self.slug = slugify(self.name)
        super(Set, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Set')
        verbose_name_plural = _('Sets')


class Image(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at'))

    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    name = SingleLineTextField(unique=True, verbose_name=_('Name'))
    public = models.BooleanField(default=True, verbose_name=_('Public'))
    image = models.ImageField(upload_to=get_image_path, max_length=4096,
                              verbose_name=_('Image'))
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                                 related_name='images',
                                 verbose_name=_('Uploader'))
    set = models.ForeignKey(Set, models.SET_NULL, blank=True, null=True,
                            related_name='images', verbose_name=_('Set'))

    def get_absolute_url(self):
        return reverse('images:image_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            orig = Image.objects.get(pk=self.pk)
            if orig.name != self.name:
                self.slug = slugify(self.name)
                path = os.path.join(settings.MEDIA_ROOT, orig.plot_file())
            if orig.image != self.image:
                path = os.path.join(settings.MEDIA_ROOT, orig.image.name)
                if os.path.exists(path):
                    os.remove(path)
        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
