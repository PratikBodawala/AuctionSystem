from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from auction.models import Item, Bid


class ItemSerializer(ModelSerializer):
    highest_bidder = serializers.SerializerMethodField()
    highest_price = serializers.SerializerMethodField()
    owner = serializers.CharField(source='owner.username', read_only=True)

    def validate_end(self, value):
        field = self.fields['start']
        if value <= field.to_internal_value(self.initial_data['start']):
            raise serializers.ValidationError('End date should be greater than start date.')
        return value

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def get_highest_price(self, obj):
        return obj.bid_set.order_by('-price').first().price if obj.bid_set.exists() else None

    def get_highest_bidder(self, obj):
        return obj.bid_set.order_by('-price').first().user.username if obj.bidders.first() else None

    class Meta:
        model = Item
        exclude = ['bidders']


class BidSerializer(ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    bidder = serializers.CharField(source='user.username', read_only=True)

    def create(self, validated_data):
        bid, _ = Bid.objects.update_or_create(user=self.context['request'].user, item=validated_data['item'],
                                              defaults=validated_data)
        return bid

    class Meta:
        model = Bid
        fields = ['price', 'item', 'item_name', 'bidder']
        read_only_fields = ['user', ]


class BidUserSerializer(ModelSerializer):
    class Meta:
        model = Bid
        fields = ['price', 'item', 'user']
