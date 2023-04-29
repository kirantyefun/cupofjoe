from rest_framework import serializers
from .models import Cafe, Order, OrderItem, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price']

class CafeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cafe
        fields = ['id', 'name', 'description',]


class CafeSerializer(serializers.ModelSerializer):
    menu = MenuItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cafe
        fields = ['id', 'name', 'description', 'menu']

    
class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField()
    def get_item_name(self, obj):
        return obj.item.name
    class Meta:
        model = OrderItem
        fields = ('item', 'quantity', 'item_name')


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    date_ordered = serializers.DateTimeField(read_only=True)
    cafe = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ('order_items', 'date_ordered', 'cafe', 'user', 'active', 'additional_instructions')
    

class OrderOutSerializer(serializers.Serializer):
    order_items = OrderItemSerializer(many=True)
    