from django.db.models import Field
from django.forms.fields import CharField

from .widgets import S3DirectWidget
from .utils import get_url


class S3DirectFile():
    def __init__(self, key):
        self.key = key
        self.url = get_url(self.key) if key else key

    def __str__(self):
        return self.url


class S3DirectFormField(CharField):
    def has_changed(self, initial, data):
        """Return True if data differs from initial."""
        # Always return False if the field is disabled since self.bound_data
        # always uses the initial value in this case.
        if self.disabled:
            return False

        if initial is not None:
            return initial.key != data

        return bool(data)


class S3DirectField(Field):
    def __init__(self, *args, **kwargs):
        dest = kwargs.pop('dest', None)
        self.widget = S3DirectWidget(dest=dest)
        super(S3DirectField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'TextField'

    def formfield(self, *args, **kwargs):
        kwargs['widget'] = self.widget
        return super(S3DirectField, self).formfield(*args, form_class=S3DirectFormField, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        return S3DirectFile(value)

    def to_python(self, value):
        if isinstance(value, S3DirectFile):
            return value

        return self.from_db_value(value, None, None)

    def get_prep_value(self, value):
        if isinstance(value, S3DirectFile):
            return value.key

        return value
