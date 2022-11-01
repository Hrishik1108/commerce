from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORY_CHOICES= [
    ('phone', 'Phone'),
    ('watches', 'Watches'),
    ('laptops', 'Laptops'),
    ('none', 'None'),
    ]
class User(AbstractUser):
    pass

class category(models.Model):
    categories=models.CharField(max_length=64)

class auction_listing(models.Model):
    name=models.CharField(max_length=64)
    price=models.FloatField()
    close=models.CharField(max_length=74,null=True)
    creation_date=models.DateTimeField()
    images=models.ImageField(upload_to="auction_image/")
    categories=models.ForeignKey(category,on_delete=models.CASCADE,null=True,related_name="cat")
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return f"{self.name}, {self.price},{self.categories}"
class WatchList(models.Model):
    watch_name=models.ForeignKey(auction_listing,on_delete=models.CASCADE,related_name="watch_name")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="watch_user")

    def __str__(self):
        return f"{self.watch_name}"
    
class Bid(models.Model):
    name=models.ForeignKey(auction_listing,on_delete=models.CASCADE,primary_key=True)
    bid=models.FloatField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bid_user")



class Comments(models.Model):
    comm_name=models.ForeignKey(auction_listing,on_delete=models.CASCADE)
    content=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comm_user")
