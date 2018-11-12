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
from .views import job


app_name = 'results'
urlpatterns = [
    path('job/', job.ListView.as_view(), name='job_list'),
    path('job/create/<int:version>/set/<int:set>/',
         job.SetCreateView.as_view(), name='job_create_set'),
    path('job/create/<int:version>/image/<int:image>/',
         job.ImageCreateView.as_view(), name='job_create_image'),
    path('job/<int:pk>/', job.DetailView.as_view(), name='job_detail'),
]
