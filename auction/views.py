from decimal import Decimal

from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from auction.models import Item, Bid
from auction.serializers import ItemSerializer, BidSerializer


# Create your views here.

class AuctionItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user)


class BidViewSet(ModelViewSet):
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return Bid.objects.filter(item_id=self.kwargs['pk'])
        return Bid.objects.filter(Q(user=self.request.user) | Q(item__owner=self.request.user))

    def create(self, request, *args, **kwargs):
        try:
            item = Item.objects.get(pk=request.data.get('item'))
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if item.end < timezone.now():
                return Response({'error': 'Auction ended'}, status=status.HTTP_400_BAD_REQUEST)
            if item.start > timezone.now():
                return Response({'error': 'Auction not started'}, status=status.HTTP_400_BAD_REQUEST)
            max_bid = item.bid_set.order_by('-price').first()

            if max_bid:
                if max_bid.price >= Decimal(request.data.get('price')):
                    return Response({'error': f'Price should be greater than {max_bid.price}'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                if item.minimum_price >= Decimal(request.data.get('price')):
                    return Response({'error': f'Price should be greater than {item.minimum_price}'},
                                    status=status.HTTP_400_BAD_REQUEST)
            return super().create(request, item, *args, **kwargs)
