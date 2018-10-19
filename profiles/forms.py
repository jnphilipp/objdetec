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

from django.contrib.auth import forms, get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class AuthenticationForm(forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['password'].help_text = mark_safe(
            '<a href="%s">%s</a>' % (
                reverse('profiles:password_reset'),
                _('Forgot your password?')
            )
        )


class UserChangeForm(forms.UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['password']. \
            help_text = mark_safe(self.fields['password'].help_text)

    class Meta(forms.UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name')


class UserCreationForm(forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1']. \
            help_text = mark_safe(self.fields['password1'].help_text)

    class Meta(forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'first_name')
