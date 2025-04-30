from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssetCategoryViewSet, AssetViewSet, AssetDetailsViewSet, AssetOutViewSet


router = DefaultRouter()
router.register('categories', AssetCategoryViewSet)
router.register('assets', AssetViewSet)
router.register('asset-details', AssetDetailsViewSet)
router.register('asset-out', AssetOutViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

