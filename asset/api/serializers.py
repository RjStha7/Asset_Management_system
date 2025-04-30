from rest_framework import serializers
from asset.models import AssetCategory, Asset, AssetDetails, AssetOut

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class AssetDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetDetails
        fields = '__all__'

class AssetOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetOut
        fields = '__all__'

