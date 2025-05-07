from django.contrib import admin

from accounts.backends import User
from accounts.models import UserProfile
from asset.models import Asset, AssetCategory, AssetDetails, AssetOut


class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Show these fields in table view
    search_fields = ('name',)      # add search by name
    list_filter = ('name',)         # add filter by name
    ordering = ('id',)           # order by name

class AssetAdmin(admin.ModelAdmin):
    list_display = ('AssetId', 'Name', 'Shortname', 'Description', 'Unit', 'AssetCategory')
    search_fields = ('Name', 'Shortname')
    list_filter = ('AssetCategory',)
    ordering = ('AssetId',)
    list_editable = ('Unit',)  # Make Unit editable in the list view
    list_per_page = 10  # Number of records per page

class AssetDetailsAdmin(admin.ModelAdmin):
    list_display = ('Sn', 'Asset', 'AssetCode','Price', 'PurchaseDate', 'Remarks', 'Status')
    search_fields = ('Asset__Name', 'Asset__Shortname')
    list_filter = ('Asset',)
    ordering = ('Sn',)
    list_per_page = 10  # Number of records per page

class AssetOutAdmin(admin.ModelAdmin):
    list_display = ('Sn', 'AssetDetail','OutTo','Outdate', 'DateToReturn', 'ReturnDate', 'Remarks')
    search_fields = ('AssetDetail__Asset__Name', 'AssetDetail__Asset__Shortname')
    list_filter = ('AssetDetail', 'OutTo')
    ordering = ('Sn',)
    list_per_page = 10  # Number of records per page

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('get_user_id', 'get_username', 'get_email', 'Phone_number', 'address')

#     def get_user_id(self, obj):
#         return obj.user.id
#     get_user_id.short_description = 'User ID'

#     def get_username(self, obj):
#         return obj.user.username
#     get_username.short_description = 'Username'

#     def get_email(self, obj):
#         return obj.user.email
#     get_email.short_description = 'Email'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'get_user_id',
        'get_username',
        'get_first_name',
        'get_last_name',
        'get_email',
        'get_is_staff',
        'get_is_active',
        'get_is_superuser',
        'get_last_login',
        'get_date_joined',
        'Phone_number',
        'address',
    )
    ordering = ('user_id',)

    def get_user_id(self, obj):
        return obj.user.id
    def get_username(self, obj):
        return obj.user.username
    def get_first_name(self, obj):
        return obj.user.first_name
    def get_last_name(self, obj):
        return obj.user.last_name
    def get_email(self, obj):
        return obj.user.email
    def get_is_staff(self, obj):
        return obj.user.is_staff
    def get_is_active(self, obj):
        return obj.user.is_active
    def get_is_superuser(self, obj):
        return obj.user.is_superuser
    def get_last_login(self, obj):
        return obj.user.last_login
    def get_date_joined(self, obj):
        return obj.user.date_joined

    # Set column headers
    get_user_id.short_description = 'User ID'
    get_username.short_description = 'Username'
    get_first_name.short_description = 'First Name'
    get_last_name.short_description = 'Last Name'
    get_email.short_description = 'Email'
    get_is_staff.short_description = 'Is Staff'
    get_is_active.short_description = 'Is Active'
    get_is_superuser.short_description = 'Is Superuser'
    get_last_login.short_description = 'Last Login'
    get_date_joined.short_description = 'Date Joined'

# Register your models here.
admin.site.register(AssetCategory, AssetCategoryAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetDetails, AssetDetailsAdmin)
admin.site.register(AssetOut, AssetOutAdmin)
admin.site.register(UserProfile, UserProfileAdmin)  # Register UserProfileAdmin