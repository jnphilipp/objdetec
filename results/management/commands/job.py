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
from keras import backend as K
from objdetec.management.base import SingleInstanceCommand
from results.models import Job


class Command(SingleInstanceCommand):
    help = 'Run object detection job.'

    def add_arguments(self, parser):
        parser.add_argument('--job', type=int)
        parser.add_argument('--batch-size', type=int, default=64)
        parser.add_argument('--data_format',
                            choices=['channels_first', 'channels_last'],
                            default=K.image_data_format())

    def handle(self, *args, **options):
        self._run_once()

        if 'job' in options and options['job']:
            job = Job.objects.get(pk=options['job'])
        else:
            job = Job.objects.filter(state='new').order_by('updated_at'). \
                first()

        if job is None:
            self._error('No job found.')
            return

        msg = '%d:\n* batch_size: %d\n* data_format: %s\n' % (
            job.pk, options['batch_size'], options['data_format'])
        self.stdout.write('Start job %d.' % job.pk)
        try:
            job.predict(options['batch_size'], options['data_format'])
            self._success('Done.')
            msg += '* state: %s' % job.state
        except Exception as e:
                self._error('Failed: %s' % e)
                job.text = str(e)
                msg += '* state: %s\n* text: %s' % (job.state, e)
        job.save()
        if msg:
            mail_admins('Job fsm', msg)
