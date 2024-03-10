from django.contrib import admin
from django.urls import path, include

from auction.views import AuctionItemViewSet, BidViewSet

urlpatterns = [
    path('auction', AuctionItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='auction-list'),
    path('auction/<int:pk>', AuctionItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='auction-detail'),
    path('auction/<int:pk>/bid', BidViewSet.as_view({'get': 'list'}), name='auction-bid'),
    path('bid', BidViewSet.as_view({'post': 'create', 'get': 'list'}), name='all-bid'),
]
