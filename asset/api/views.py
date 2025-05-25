from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from asset.models import AssetCategory, Asset, AssetDetails, AssetOut
from .serializers import (
    AssetCategorySerializer,
    AssetSerializer, 
    AssetDetailsSerializer, 
    AssetOutSerializer, 
    
)

class AssetCategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = AssetCategory.objects.all().order_by('id')
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['name']  # rfilterable fields
    # search_fields = ['name', 'description']  # searchable fields

class AssetViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Asset.objects.all().order_by('AssetId')
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class AssetDetailsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = AssetDetails.objects.all().order_by('Sn')
    queryset = AssetDetails.objects.all()
    serializer_class = AssetDetailsSerializer
    
class AssetOutViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = AssetOut.objects.all().order_by('Sn')
    queryset = AssetOut.objects.all()
    serializer_class = AssetOutSerializer