from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import models
from django import forms

from .models import Auction, Bid, Comment, User, Watchlist, CATEGORIES
from .forms import NewAuctionForm, NewBidForm, NewCommentForm, WatchlistForm


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.exclude(is_active=False).all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def add(request):
    if request.method == "POST":
        form = NewAuctionForm(request.POST, request.FILES)
        if form.is_valid():
            new_auction = form.save(commit=False)
            new_auction.owner = request.user
            new_auction.initial_price = new_auction.price
            new_auction.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("Error") 
    return render(request, "auctions/add.html", {
        "auction": NewAuctionForm()
        })


def auction(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    return render(request, "auctions/auction.html", {
        "auction": auction,
        "bid_form": NewBidForm(),
        "comment_form": NewCommentForm(),
        "comments": auction.comments.all(),
        "bids": auction.bids.all(),
        "user": request.user,
    })


@login_required(login_url='login')
def bids(request, auction_id):
    if request.method == "POST":
        form = NewBidForm(request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)
            auction = Auction.objects.get(pk=auction_id)
            person = request.user
            if new_bid.price > auction.price or (new_bid.price == auction.initial_price and not auction.bids.all()):
                new_bid.auction = auction
                new_bid.person = person
                new_bid.save()
                auction.price = new_bid.price
                auction.save()
            else:
                return HttpResponse(f"<h1>You can not set price, which is not bigger than {auction.price}</h1>")
        return HttpResponseRedirect(reverse("auction", args=(auction_id,)))


@login_required(login_url='login')
def comments(request, auction_id):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            auction = Auction.objects.get(pk=auction_id)
            author = request.user
            new_comment.auction = auction
            new_comment.author = author
            new_comment.save()
        return HttpResponseRedirect(reverse("auction", args=(auction_id,)))


def categories_list(request):
    return render(request, "auctions/categories.html", {
        "categories": CATEGORIES
    })


def show_category(request, category_name):
    auctions = Auction.objects.filter(category=category_name).exclude(is_active=False).all()
    return render(request, "auctions/category.html", {
        "auctions": auctions,
        "name": category_name
    })


@login_required(login_url='login')
def add_to_watchlist(request, user_id):
    if request.method == "POST":
        user = User.objects.get(pk=user_id)
        auction_id = request.POST.get("watchlist_add")
        auction = Auction.objects.get(pk=auction_id)
        watchlist = Watchlist()
        watchlist.user = user
        watchlist.item = auction
        watchlist.save()
    return HttpResponseRedirect(reverse("watchlist", args=(user_id,)))


@login_required(login_url='login')
def watchlist(request, user_id):
    user = User.objects.get(pk=user_id)
    watchlists = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "watchlists": watchlists
    })


@login_required(login_url='login')
def watchlist_delete(request, watchlist_id):
    if request.method == "POST":
        Watchlist.objects.get(pk=watchlist_id).delete()
    return HttpResponseRedirect(reverse("watchlist", args=(request.user.id,)))


def close(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=auction_id)
        max_bid = None
        for bid in auction.bids.all():
            if max_bid and bid.price > max_bid.price:
                max_bid = bid
            elif not max_bid:
                max_bid = bid
        if max_bid:
            auction.winner = max_bid.person
        auction.is_active = False
        auction.save()
    return HttpResponseRedirect(reverse("auction", args=(auction_id,)))
    