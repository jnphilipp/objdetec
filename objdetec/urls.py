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

"""objdetec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView, TemplateView

from . import views
from .decorators import piwik

admin.site.site_header = _('objdetec administration')


urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('legal_notice/', piwik('Legal notice • objdetec')(
        TemplateView.as_view(template_name='objdetec/legal_notice.html')),
         name='legal_notice'),
    path('privacy_policy/', piwik('Privacy policy • objdetec')(
        TemplateView.as_view(template_name='objdetec/privacy_policy.html')),
         name='privacy_policy'),

    path('admin/', admin.site.urls),
    path('images/', include('images.urls')),
    path('nnmodels/', include('nnmodels.urls')),
    path('profile/', include('profiles.urls')),
    path('results/', include('results.urls')),

    path('favicon.ico', RedirectView.as_view(url='/static/images/icon.png')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
