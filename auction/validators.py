from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils import timezone


def minimum_price_validator(value: Decimal):
    if value < 0:
        raise ValidationError('Minimum price cannot be negative')


def start_date_validator(value):
    if value < timezone.now():
        raise ValidationError('Start date cannot be in the past')
