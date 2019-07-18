from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Shop, Department, Item


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'is_staff', 'is_superuser')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ItemSerializerForAdmin(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ItemSerializerForDefinedUsers(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'is_sold', 'comments', 'department')


class ItemSerializerForUndefinedUsers(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'description', 'is_sold', 'comments', 'department')


class ItemSerializerForAnonymous(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'description', 'is_sold')


class DepartmentSerializerForAdmin(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DepartmentSerializerForDefinedUsers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('sphere', 'staff_amount', 'shop')


class DepartmentSerializerForUndefinedUsers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('sphere', 'shop')


class ShopSerializerForAdmin(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class ShopSerializerForDefinedUsers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = ('name', 'address', 'staff_amount')


class ShopSerializerForUndefinedUsers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = ('name', 'address')
