from decimal import Decimal

from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel

from auction.validators import minimum_price_validator, start_date_validator


# Create your models here.

class Item(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    minimum_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[minimum_price_validator], default=Decimal('0'), blank=True)
    owner = models.ForeignKey('auth.User', related_name='items', on_delete=models.CASCADE)
    start = models.DateTimeField(validators=[start_date_validator])
    end = models.DateTimeField()
    bidders = models.ManyToManyField('auth.User', through='Bid', related_name='bids')

    def clean(self):
        if self.end <= self.start:
            raise ValidationError('End date should be greater than start date')

    def __str__(self):
        return self.name


class Bid(TimeStampedModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.user} - {self.item} - {self.price}'

    class Meta:
        unique_together = ('item', 'user')
        ordering = ['-price']


# @receiver(signals.pre_save)
# def pre_save_handler(sender, instance, *args, **kwargs):
#     if sender is not Session:
#         instance.full_clean()
