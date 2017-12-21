#encoding:utf-8

from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ImproperlyConfigured, ValidationError


class MinLenValidator(MinimumLengthValidator):

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                u'密码长度太短，至少要8个字符！',
                code='password_too_short',
                params={'min_length': self.min_length},
            )



