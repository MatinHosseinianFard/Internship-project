from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class RegNumberValidator(validators.RegexValidator):
    pass
