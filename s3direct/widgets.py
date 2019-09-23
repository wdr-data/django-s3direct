from __future__ import unicode_literals

import os

from django.forms import widgets
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlunquote_plus
from django.conf import settings

from .types import S3DirectFile


class S3DirectWidget(widgets.TextInput):
    class Media:
        js = ('s3direct/dist/index.js', )
        css = {'all': ('s3direct/dist/index.css', )}

    def __init__(self, *args, **kwargs):
        self.dest = kwargs.pop('dest', None)
        super(S3DirectWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):
        if isinstance(value, S3DirectFile):
            file_key = value.key
            file_url = value.url
            file_name = value.key
        else:  # TODO
            print('Unknown value type "', type(value), '" with value', value)
            file_key = ''
            file_url = ''
            file_name = ''

        csrf_cookie_name = getattr(settings, 'CSRF_COOKIE_NAME', 'csrftoken')

        ctx = {
            'policy_url': reverse('s3direct'),
            'signing_url': reverse('s3direct-signing'),
            'dest': self.dest,
            'name': name,
            'csrf_cookie_name': csrf_cookie_name,
            'file_key': file_key,
            'file_url': file_url,
            'file_name': file_name,
        }

        return mark_safe(
            render_to_string(os.path.join('s3direct', 's3direct-widget.tpl'),
                             ctx))
