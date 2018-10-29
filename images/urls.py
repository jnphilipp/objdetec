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
from .views import image, set


app_name = 'images'
urlpatterns = [
    path('image/', image.ListView.as_view(), name='image_list'),
    path('image/<int:page>/', image.ListView.as_view()),
    path('image/create/', image.CreateView.as_view(),
         name='image_create'),
    path('image/<slug:slug>/', image.DetailView.as_view(),
         name='image_detail'),
    path('image/<slug:slug>/update/', image.UpdateView.as_view(),
         name='image_update'),

    path('set/create/', set.CreateView.as_view(), name='set_create'),
    path('set/<slug:slug>/', set.DetailView.as_view(), name='set_detail'),
    path('image/<slug:slug>/result/', image.DetailView.as_view(),
         name='image_results'),
    path('image/<slug:slug>/result/<int:result_id>/',
         image.DetailView.as_view(), name='image_result'),
    path('set/<slug:slug>/update/', set.UpdateView.as_view(),
         name='set_update'),
]
