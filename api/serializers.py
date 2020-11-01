from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Product, Location, Transfer, HistoryOfTransfer, HistoryOfLoginToZakuro


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['id', 'product', 'location', 'pcs', 'user', 'last_transfer', 'location_name', 'product_name',
                  'product_index', 'user_name']

class HistoryOfTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryOfTransfer
        fields = ['id', 'product', 'locationFrom', 'locationTo', 'pcs', 'user', 'date_transfer', 'location_name_from',
                  'location_name_to', 'product_name','product_index', 'user_name']
# //////////////////FOR ZAKURO/////////////////////////////////////////////////////
class HistoryOfLoginToZakuroSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryOfLoginToZakuro
        fields = '__all__'
# //////////////////FOR DENTIST/////////////////////////////////////////////////////
