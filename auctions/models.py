from django.contrib.auth.models import AbstractUser
from django.db import models


CATEGORIES = [
    ('books', 'Books'),
    ('clothing', 'Clothing'),
    ('shoes', 'Shoes'),
    ('electronics', 'Electronics'),
    ('household products', 'Household products'),
    ('sports', 'Sports'),
    ('tourism', 'Tourism'),
    ('other', 'Other')
    ]


class User(AbstractUser):
    pass


class Auction(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=64, choices=CATEGORIES, default=CATEGORIES[7]) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} --  price: {self.price}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)


class Bid(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    person = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"<b>{self.person}</b> set price: {self.price}"


class Comment(models.Model):
    comment = models.TextField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"<b>{self.author}</b>: {self.comment}"
