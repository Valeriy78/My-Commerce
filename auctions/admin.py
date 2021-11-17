from django.contrib import admin
from .models import Bid, User, Auction, Comment, Watchlist

# Register your models here.
admin.site.register(Auction)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
