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
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Version


@receiver(pre_delete, sender=Version)
def delete_files(sender, instance, **kwargs):
    os.remove(os.path.join(settings.MEDIA_ROOT, instance.model_file.name))
    os.remove(os.path.join(settings.MEDIA_ROOT,
                           instance.trainhistory_file.name))
