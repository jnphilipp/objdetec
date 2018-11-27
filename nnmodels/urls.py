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
from objdetec.decorators import piwik

from .views import nnmodel, version


app_name = 'nnmodels'
urlpatterns = [
    path('nnmodel/', nnmodel.ListView.as_view(), name='nnmodel_list'),
    path('nnmodel/<int:page>/', nnmodel.ListView.as_view()),
    path('nnmodel/create/', nnmodel.CreateView.as_view(),
         name='nnmodel_create'),
    path('nnmodel/<slug:slug>/', nnmodel.DetailView.as_view(),
         name='nnmodel_detail'),
    path('nnmodel/<slug:slug>/edit/', nnmodel.UpdateView.as_view(),
         name='nnmodel_edit'),

    path('nnmodel/<slug:slug>/create/', version.CreateView.as_view(),
         name='version_create'),
    path('nnmodel/<slug:slug>/<int:pk>/',
         piwik('Version • NN Model • N Models • objdetec')(
            version.DetailView.as_view()), name='version_detail'),
    path('nnmodel/<slug:slug>/<int:pk>/config/',
         piwik('Config • Version • NN Model • N Models • objdetec')(
            version.DetailView.as_view()), name='version_config'),
    path('nnmodel/<slug:slug>/<int:pk>/plot/',
         piwik('Plot • Version • NN Model • N Models • objdetec')(
            version.DetailView.as_view()), name='version_plot'),
    path('nnmodel/<slug:slug>/<int:pk>/edit/',
         version.UpdateView.as_view(), name='version_edit'),
    path('nnmodel/<slug:slug>/<int:pk>/charts/trainhistory/',
         version.charts.trainhistory, name='version_chart_trainhistory'),
]
