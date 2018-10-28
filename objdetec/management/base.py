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

import fcntl
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand


class SingleInstanceCommand(BaseCommand):
    def _run_once(self):
        host_script_file_path = os.path.realpath(sys.argv[0])
        settings.RUN_ONCE_FILE_HANDLE = open(host_script_file_path, 'r')
        try:
            fcntl.flock(settings.RUN_ONCE_FILE_HANDLE,
                        fcntl.LOCK_EX | fcntl.LOCK_NB)
        except:
            self._error('Another instance is already running.')
            sys.exit(1)

    def _success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def _error(self, msg):
        self.stdout.write(self.style.ERROR(msg))
