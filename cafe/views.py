from django.db.utils import IntegrityError
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .exceptions import custom_exception
from .models import Cafe, Order, OrderItem
from .permissions import CafeOwnerRequired, CanCreateCafe, HasCafeRegistered
from .serializers import (CafeListSerializer, CafeSerializer,
                          MenuItemSerializer, OrderSerializer)


class CafeViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated, CanCreateCafe]
        elif self.action == 'place_order':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, CafeOwnerRequired]
        return [permission() for permission in permission_classes]

    queryset = Cafe.objects.prefetch_related("menu_items")

    def get_serializer_class(self):
        if self.action == "list":
            return CafeListSerializer
        return CafeSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        cafe = serializer.save(owner=request.user)
        request.user.has_cafe_registered = True
        request.user.save(update_fields=["has_cafe_registered"])
        return Response(serializer_class(cafe).data)
    
    @action(methods=['POST'], detail=True, url_path='place-order')
    def place_order(self, request, pk):
        order_serializer = OrderSerializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)
        cafe = self.get_object()
        user = request.user
        order_items = order_serializer.validated_data.pop('order_items')
        order = Order.objects.create(user=user, cafe=cafe, **order_serializer.validated_data)
        for item in order_items:
            OrderItem.objects.create(order=order, **item)

        # TODO: send email to let user and cafe owner know about order
        return Response(OrderSerializer(order).data)
    
    @action(detail=True, url_path='view-orders')
    def view_orders(self, request, pk):
        cafe = self.get_object()
        orders = cafe.orders.all()
        return Response(OrderSerializer(orders, many=True).data)


class MenuItemViewSet(ModelViewSet):
    """
    cafe owner permission is required to use operations in this viewset
    """

    permission_classes = [permissions.IsAuthenticated, HasCafeRegistered]

    def get_queryset(self):
        return self.request.user.cafe.menu

    serializer_class = MenuItemSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                menu_item = serializer.save(cafe=request.user.cafe)
            except IntegrityError:
                return custom_exception(
                    "Same Item can not be added more than once.",
                    status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer_class(menu_item).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        menu_item = self.get_object()
        seriailizer = self.serializer_class(data=request.data, instance=menu_item)
        seriailizer.is_valid(raise_exception=True)
        menu_item = seriailizer.save()
        return Response(self.serializer_class(menu_item).data)

    def partial_update(self, request, *args, **kwargs):
        menu_item = self.get_object()
        seriailizer = self.serializer_class(
            data=request.data, instance=menu_item, partial=True
        )
        seriailizer.is_valid(raise_exception=True)
        menu_item = seriailizer.save()
        return Response(self.serializer_class(menu_item).data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Throw 405 error status code for put request
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
