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

import sys

from django.conf import settings
from functools import wraps
from piwikapi.tracking import PiwikTracker
from urllib.error import HTTPError


def piwik(title):
    def piwik_decorator(func):
        @wraps(func)
        def func_wrapper(request, *args, **kwargs):
            if check_piwik_settings():
                try:
                    piwik = PiwikTracker(settings.PIWIK['SITE_ID'], request)
                    piwik.set_api_url('%s/piwik.php' % settings.PIWIK['URL'])
                    piwik.set_ip(get_client_ip(request))
                    piwik.set_token_auth(settings.PIWIK['AUTH_TOKEN'])
                    if request.user.is_authenticated:
                        piwik.set_visitor_id(request.user.unique_visitor_id)
                    piwik.do_track_page_view(title)
                except HTTPError as e:
                    sys.stderr.write(str(e))
                    sys.stderr.write('\n')

            return func(request, *args, **kwargs)
        return func_wrapper
    return piwik_decorator


def check_piwik_settings():
    if 'SITE_ID' in settings.PIWIK and 'URL' in settings.PIWIK and \
             'AUTH_TOKEN' in settings.PIWIK:
        if settings.PIWIK['SITE_ID'] and settings.PIWIK['URL'] and \
                settings.PIWIK['AUTH_TOKEN']:
            return True
    return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')
