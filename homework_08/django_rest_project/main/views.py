from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import UserSerializer, ItemSerializerForDefinedUsers,\
    ItemSerializerForUndefinedUsers, ItemSerializerForAnonymous, DepartmentSerializerForDefinedUsers,\
    DepartmentSerializerForUndefinedUsers, ShopSerializerForDefinedUsers, ShopSerializerForUndefinedUsers,\
    ShopSerializerForAdmin, DepartmentSerializerForAdmin, ItemSerializerForAdmin
from .models import Item, Department, Shop
from .permissions import IsStaff, IsUserWithNameAndSurname, IsUserWithoutNameAndSurname,\
    IsAnonymous, AdminAccessPermission, StaffAccessPermission


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined')


class ActiveItemView(APIView):

    def get(self, request):
        items = Item.objects.filter(is_sold=False)
        serializer_data = {'response': '403 Forbidden'}, 403

        if request.user.is_superuser:
            serializer_data = ItemSerializerForDefinedUsers(items, many=True, context={'request': request}).data

        return Response(serializer_data)

    @action(method=['delete'], detail=False)
    def delete(self, request, detail=False):
        if request.user.is_superuser:
            Item.objects.all().delete()
            return Response({'response': '200 OK'})
        else:
            return Response({'response': '403 Forbidden'})


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.order_by("id")
    permission_classes = [IsStaff | IsUserWithNameAndSurname | IsUserWithoutNameAndSurname | IsAnonymous]

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter(is_sold=False)

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return ItemSerializerForAdmin

        elif self.request.user.is_anonymous:
            return ItemSerializerForAnonymous

        elif self.request.user.is_staff or len(self.request.user.first_name):
            return ItemSerializerForDefinedUsers

        else:
            return ItemSerializerForUndefinedUsers


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.order_by("id")
    permission_classes = [IsStaff | IsUserWithNameAndSurname | IsUserWithoutNameAndSurname]

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.annotate(item_sold_ammount=Count('items', filter=Q(items__is_sold=False)))\
                .filter(item_sold_ammount=0)
            queryset = queryset.annotate(item_amount=Count('items'))\
                .filter(item_amount__gt=0)

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return DepartmentSerializerForAdmin

        elif self.request.user.is_staff or len(self.request.user.first_name):
            return DepartmentSerializerForDefinedUsers

        else:
            return DepartmentSerializerForUndefinedUsers


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.order_by("id")
    permission_classes = [IsStaff | IsUserWithNameAndSurname | IsUserWithoutNameAndSurname]

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.annotate(
                item_sold_ammount=Count('departments__items__is_sold', filter=Q(departments__items__is_sold=False))
            ).filter(item_sold_ammount=0)
            queryset = queryset.annotate(item_ammount=Count('departments__items')).filter(item_ammount__gt=0)
        return queryset

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return ShopSerializerForAdmin

        elif self.request.user.is_staff or len(self.request.user.first_name):
            return ShopSerializerForDefinedUsers

        else:
            return ShopSerializerForUndefinedUsers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminAccessPermission | StaffAccessPermission]
