from rest_framework import serializers
from asset.models import AssetCategory, Asset, AssetDetails, AssetOut
from django.contrib.auth.models import User

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    AssetCategoryName = serializers.CharField(source='AssetCategory.name', read_only=True)
    AssetCategory = serializers.PrimaryKeyRelatedField(queryset=AssetCategory.objects.all())

    class Meta:
        model = Asset
        fields = [
            'AssetId',
            'Name',
            'Shortname',
            'Description',
            'Unit',
            'AssetCategory',
            'AssetCategoryName',
        ]

class AssetDetailsSerializer(serializers.ModelSerializer):
    AssetName = serializers.CharField(source='Asset.Name', read_only=True)
    Asset = serializers.PrimaryKeyRelatedField(queryset=Asset.objects.all())

    class Meta:
        model = AssetDetails
        fields = [
            'Sn',
            'Asset',
            'AssetCode',
            'Price',
            'PurchaseDate',
            'Remarks',
            'Status',
            'AssetName',
        ]

class UserinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class AssetOutSerializer(serializers.ModelSerializer):
    AssetCodeName = serializers.CharField(source='AssetDetail.AssetCode', read_only=True)
    OutToName = serializers.CharField(source='OutTo.username', read_only=True)

    AssetDetail = serializers.PrimaryKeyRelatedField(queryset=AssetDetails.objects.all())
    OutTo = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


    class Meta:
        model = AssetOut
        fields = [
            'Sn',
            'AssetDetail',
            'OutTo',
            'Outdate',
            'DateToReturn',
            'ReturnDate',
            'Remarks',
            'AssetCodeName',
            'OutToName',
            
        ]

