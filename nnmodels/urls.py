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

from django.urls import path
from . import views


app_name = 'nnmodels'
urlpatterns = [
    path('nnmodel/', views.nnmodel.list, name='nnmodels'),
    path('nnmodel/<slug:slug>/', views.nnmodel.detail, name='nnmodel'),
    path('nnmodel/<slug:slug>/<int:version_id>/', views.version.detail,
         name='version'),
    path('nnmodel/<slug:slug>/<int:version_id>/config/', views.version.config,
         name='version_config'),
    path('nnmodel/<slug:slug>/<int:version_id>/plot/', views.version.plot,
         name='version_plot'),
    path('nnmodel/<slug:slug>/<int:version_id>/charts/trainhistory/',
         views.version.charts.trainhistory, name='version_chart_trainhistory'),
]
