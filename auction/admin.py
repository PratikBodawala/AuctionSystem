from django.contrib import admin

from auction.models import Item
from auction.models import Bid


# Register your models here.
admin.site.register(Item)
admin.site.register(Bid)
