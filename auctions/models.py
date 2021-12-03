from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# class Category(models.Model):
#     category = models.Charfield(max_lentgh=64)

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    starting_bid = models.FloatField()
    current_bid = models.FloatField(blank=True, null=True)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="owner", null=True)
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="buyer", null=True)
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

class Bids(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField(blank=True, null=True)

class Comment(models.Model):
    comment = models.CharField(max_length=200)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name = "comment1")
