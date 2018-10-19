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

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from objdetec.fields import SingleLineTextField

from .user_manager import UserManager


def default_unique_visitor_id():
    return ''.join(['%02x' % h for h in os.urandom(8)])


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )

    email = models.EmailField(
        unique=True,
        verbose_name=_('Email')
    )
    first_name = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=_('First name')
    )
    last_name = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=_('Last name')
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Date joined')
    )
    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. ' +
            'Unselect this instead of deleting accounts.'
        ),
    )
    unique_visitor_id = models.CharField(
        max_length=16,
        default=default_unique_visitor_id,
        unique=True,
        verbose_name=_('Unique visitor ID')
    )

    def get_absolute_url(self):
        return reverse('profiles:profile')

    def __str__(self):
        return self.get_short_name()

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name if self.first_name else self.email

    class Meta:
        ordering = ('email',)
        verbose_name = _('User')
        verbose_name_plural = _('Users')
