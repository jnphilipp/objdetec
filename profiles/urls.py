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


app_name = 'profiles'
urlpatterns = [
    path('', views.profile, name='profile'),

    path('password/', views.password_change, name='password_change'),
    path('password/done/', views.password_change_done,
         name='password_change_done'),
    path('password/reset/', views.password_reset, name='password_reset'),
    path('password/reset/done/', views.password_reset_done,
         name='password_reset_done'),
    path('password/reset/complete/', views.password_reset_complete,
         name='password_reset_complete'),
    path('password/reset/confirm/<uidb64>/<token>/',
         views.password_reset_confirm, name='password_reset_confirm'),

    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
]
