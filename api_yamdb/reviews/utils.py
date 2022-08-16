from django.core.exceptions import ValidationError
from django.utils import timezone
from pkg_resources import _


def year_validator(value):
    if value < 1900 or value > timezone.now().year:
        raise ValidationError(
            _('%(value)s указан некорректный год!'),
            params={'value': value},
        )
