from django.db.models import CASCADE
from django.db import models
from django.contrib.auth.models import User

#NOW WE WILL CREATE A NEW MODEL FOR ASSET MANAGEMENT SYSTEM
class AssetCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='default_name', unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "AssetCategory"
        verbose_name_plural = "AssetCategories"
    

class Asset(models.Model):
    AssetId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100, default='default_name', unique = True)
    Shortname = models.CharField(max_length=50, unique = True)
    Description = models.CharField(max_length=200, blank = True)
    Unit = models.CharField(max_length=50, null=True)
    AssetCategory = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
    
class AssetDetails(models.Model):
    Sn = models.AutoField(primary_key=True)
    Asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    AssetCode = models.CharField(max_length=50, unique=True)
    Price = models.FloatField(null=False)
    PurchaseDate = models.DateField()
    Remarks = models.CharField(max_length=200, blank=True)
    STATUS_CHOICES =[
        ('working', 'Working'),
        ('not_working', 'Not Working'),
        ('damaged', 'Damaged'),
        ('lost', 'Lost'),
        ('in_repair', 'In Repair'),
        ('disposed', 'Disposed'),
    ]
    Status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Working')
    
    def __str__(self):
        return self.AssetCode
    
    class Meta:
        verbose_name = "AssetDetails"
        verbose_name_plural = "AssetDetails"
    
class AssetOut(models.Model):
    Sn = models.AutoField(primary_key=True)
    AssetDetail = models.ForeignKey(AssetDetails, on_delete=models.CASCADE)
    OutTo = models.ForeignKey(User,on_delete=models.CASCADE )
    Outdate = models.DateField()
    DateToReturn = models.DateField()
    ReturnDate = models.DateField()
    Remarks = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.AssetDetail.AssetCode} - {self.Outdate}"
    
    class Meta:
        verbose_name = "AssetOut"
        verbose_name_plural = "AssetOut"
    