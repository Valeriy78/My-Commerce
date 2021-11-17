from django import forms
from django.db.models import fields
from .models import *


class NewAuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('name', 'image', 'description', 'category', 'price')


class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('price',)


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


class WatchlistForm(forms.Form):
    auction_id = forms.IntegerField()
