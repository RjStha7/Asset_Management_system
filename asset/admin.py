from django.contrib import admin

from accounts.models import UserProfile
from asset.models import Asset, AssetCategory, AssetDetails, AssetOut

# Register your models here.
admin.site.register(AssetCategory)
admin.site.register(Asset)
admin.site.register(AssetDetails)
admin.site.register(AssetOut)
admin.site.register(UserProfile)