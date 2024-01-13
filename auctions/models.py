from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.categoryName}"
    

class Bid(models.Model):
    bid = models.IntegerField(default=0)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    imageUrl = models.CharField(max_length=2000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidprice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category_listing = models.ForeignKey(category, on_delete=models.CASCADE, null=True, blank=True, related_name="listing2")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="cart")
    
    
    def __str__(self):
        return f"{self.title}"
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"


  

