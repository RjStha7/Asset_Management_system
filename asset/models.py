from django.db.models import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

#NOW WE WILL CREATE A NEW MODEL FOR ASSET MANAGEMENT SYSTEM
class AssetCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "AssetCategory"
        verbose_name_plural = "AssetCategories"
        ordering = ['id']
    

class Asset(models.Model):
    AssetId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100, unique = True)
    Shortname = models.CharField(max_length=50, unique = True)
    Description = models.CharField(max_length=500, blank = True)
    Unit = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    AssetCategory = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)

    class Meta:
        ordering = ['AssetId']
    
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
        ('available', 'Available'),
        ('not_available', 'Not Available'),
        ('in_use', 'In Use'),
        ('damaged', 'Damaged'),
        ('lost', 'Lost'),
        ('in_repair', 'In Repair'),
        ('disposed', 'Disposed'),
    ]
    Status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Working')

    def save(self, *args, **kwargs):
        if not self.pk:
            # New instance, increment Unit
            self.Asset.Unit += 1
            self.Asset.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Decrement Unit on delete (but not below zero)
        if self.Asset.Unit > 0:
            self.Asset.Unit -= 1
            self.Asset.save()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.AssetCode
    
    class Meta:
        verbose_name = "AssetDetails"
        verbose_name_plural = "AssetDetails"
        ordering = ['Sn']
    
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
        ordering = ['Sn']
    