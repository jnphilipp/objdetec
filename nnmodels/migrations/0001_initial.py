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
# Generated by Django 2.0.4 on 2018-05-02 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import objdetec.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NNModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('name', objdetec.fields.SingleLineTextField(unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('public', models.BooleanField(default=True, verbose_name='Public')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nnmodels', to=settings.AUTH_USER_MODEL, verbose_name='Uploader')),
            ],
            options={
                'verbose_name': 'NN Model',
                'verbose_name_plural': 'NN Models',
                'ordering': ('name',),
            },
        ),
    ]
