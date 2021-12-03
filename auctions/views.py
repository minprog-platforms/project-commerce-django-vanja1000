from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import *


def index(request):
    listing = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listing
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
            # return HttpResponseRedirect(reverse("index"))
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    # return HttpResponseRedirect(reverse("index"))
    return redirect("index")


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

@login_required
def create_listing(request):
    if request.method == "POST":
        listing = AuctionListing()
        listing.title = request.POST["title"]
        listing.description = request.POST["description"]
        listing.starting_bid = request.POST["starting_bid"]
        listing.image = request.POST["URL"]
        listing.category = request.POST["category"]
        listing.owner = request.user
        listing.save()
        # return render(request, "auctions/index.html", {
        #     "listings": [listing]
        # })
        return redirect("index")

    return render(request, "auctions/create_listing.html")

def listing_page(request, listing_id):
    listing_page = AuctionListing.objects.get(id=listing_id)
    user = request.user 
    return render(request, "auctions/listing_page.html", {
        "listing": listing_page,
        "in_watchlist": user in listing_page.watchlist.all(),
        "owner": user == listing_page.owner,
        "customer": user == listing_page.customer
    })

@login_required
def watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "listings": watchlist
    })

@login_required
def add_watchlist(request, listing_id):
    listing_page = AuctionListing.objects.get(id=listing_id)
    user = request.user
    listing_page.watchlist.add(user)
    listing_page.save()
    # return HttpResponseRedirect(reverse("listing_page", args=(listing_page.id,)))
    return redirect("listing_page", listing_id)


@login_required
def remove_watchlist(request, listing_id):
    listing_page = AuctionListing.objects.get(id=listing_id)
    user = request.user
    listing_page.watchlist.remove(user)
    listing_page.save()
    # return HttpResponseRedirect(reverse("listing_page", args=(listing_page.id,)))
    return redirect("listing_page", listing_id)


@login_required
def offer(request, listing_id):
    listing_page = AuctionListing.objects.get(id=listing_id)
    user = request.user
    bid = Bids()
    if request.method == "POST":

        # form = AddBid(request.POST)

        user_bid = float(request.POST["user_offer"])
        print(user_bid)
        print(listing_page.starting_bid)
        print(listing_page.current_bid)

        if user_bid >= listing_page.starting_bid:

            if listing_page.current_bid is None or user_bid > listing_page.current_bid: 
                listing_page.current_bid = user_bid
                bid.bid = user_bid
                bid.user = user
                bid.listing = listing_page
                bid.save()
                listing_page.save()
                return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

            else:
                return render(request, "auctions/error_message.html")
        else:
            return render(request, "auctions/error_message.html")
    # else:
    listing = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
            "listings": listing
        })

@login_required
def close(request, listing_id):
    listing_page = AuctionListing.objects.get(id=listing_id)
    if request.user == listing_page.owner:
        listing_page.active = False
        listing_page.save()
        return redirect("listing_page", listing_id)
    else:
        listing = AuctionListing.objects.filter(active=True)
        return render(request, "auctions/index.html", {
            "listings": listing
        })
    
@login_required
def comments(request, listing_id):
    listings = AuctionListing.objects.get(id=listing_id)
    # comments = Comment.objects.filter(id=listing_id)
    comments = Comment()
    if request.method =="POST":
        comments.comment = request.POST["your_comment"]
        comments.user = request.user
        comments.listing = listings
        comments.save()
        print(comments.comment)
        # return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
        return redirect("listing_page", listing_id)
        # return render(request, "auctions/listing_page.html", {
        # "comments": comments,
        # "listing": listing_page,
        # "in_watchlist": request.user in listing_page.watchlist.all(),
        # "owner": request.user == listing_page.owner,
        # "customer": request.user == listing_page.customer
        # })
    else:
        return redirect("index")


    







