from django.db import models

# Create your models here.


class category(models.Model):
    category=models.CharField(max_length=50)
    def __str__(self):
        return self.category

class perfume(models.Model):
    
    perfumename=models.CharField(max_length=100)
    perfumebrand=models.CharField(max_length=100)
    perfume_details=models.CharField(max_length=500)
    perfume_price=models.IntegerField()
    perfume_image=models.FileField(upload_to='cover')
    perfume_stock=models.IntegerField()
    perfume_scent=models.CharField(max_length=50)
    perfume_volume=models.CharField(max_length=50)
    perfume_category=models.ForeignKey(category,on_delete=models.CASCADE)
    
class rating(models.Model):
    rating=models.CharField(max_length=100)
    def __str__(self):
        return self.rating
    
# python-dotenv
# 
    
   