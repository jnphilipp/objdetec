
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

from django.core.mail import mail_admins
from django.core.management.base import BaseCommand
from nnmodels.models import Version


class Command(BaseCommand):
    help = 'Run fsm transition on Versions.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        msg = ''
        for version in Version.objects.filter(state='new'):
            self.stdout.write('* %s' % version)

            try:
                version.update_from_model()
                self.stdout.write(self.style.SUCCESS('* %s: success.' %
                                                     version))
                msg += '* %s: done.\n' % version
            except Exception as e:
                self.stdout.write(self.style.ERROR('* %s: failed.' % version))
                self.stderr.write(self.style.ERROR('    %s' % e))
                msg += '* %s: failed\n' % version
                msg += '    %s\n' % e
            version.save()

        if msg:
            mail_admins('NNModel versions fsm', msg)
