from django.db import models  

class Category(models.Model):
    CategoryName = models.CharField(max_length=100, blank=True)
    Status = models.IntegerField(default=0, blank=True)      
    CreatedDate = models.CharField(max_length=30, blank=True)
    CreatedTime = models.CharField(max_length=30, blank=True)
    UpdatedDate = models.CharField(max_length=30, blank=True)
    UpdatedTime = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return self.CategoryName
    
class Item(models.Model):
    CodeType = models.CharField(max_length=30, blank=True)
    ItemName = models.CharField(max_length=30, blank=True)
    ItemCode = models.CharField(max_length=30, blank=True)
    CatID = models.ForeignKey(Category, on_delete=models.CASCADE)
    Inventory = models.IntegerField(default=0, blank=True)
    Description = models.CharField(max_length=250, blank=True)
    UnitPrice = models.FloatField(default=0, blank=True)
    UoS = models.CharField(max_length=100, blank=True)
    Packing = models.CharField(max_length=100, blank=True)
    Currency = models.CharField(max_length=30, blank=True)
    HSN = models.CharField(max_length=30, blank=True)
    TaxCode = models.FloatField(default=0, blank=True)
    Discount = models.FloatField(default=0, blank=True)
    Status = models.IntegerField(default=0, blank=True)      
    CreatedDate = models.CharField(max_length=30, blank=True)
    CreatedTime = models.CharField(max_length=30, blank=True)
    UpdatedDate = models.CharField(max_length=30, blank=True)
    UpdatedTime = models.CharField(max_length=30, blank=True)

class Tax(models.Model):
    TaxName = models.CharField(max_length=30, blank=True)
    TaxCode = models.FloatField(default=0, blank=True)
    CreatedDate = models.CharField(max_length=30, blank=True)
    CreatedTime = models.CharField(max_length=30, blank=True)

