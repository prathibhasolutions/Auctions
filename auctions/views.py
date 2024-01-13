from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . models import User,Listing,category,Comment,Bid


def index(request):
    activelistings = Listing.objects.filter(isActive=True)
    allCategories = category.objects.all()
    return render(request, "auctions/index.html",{
        "Listings": activelistings,
        "categories": allCategories,
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

def CreateListing(request):
    if request.method == "GET":
        allcategories = category.objects.all()
        return  render(request,"auctions/create.html", {
            "categories": allcategories,
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageUrl = request.POST["imageUrl"]
        price = request.POST["price"]
        v1 = request.POST['v1']
        currentUser = request.user
        
       
        categoryData = category.objects.get(categoryName = v1)

        bid = Bid(bid=float(price), by_user=currentUser)
        
        bid.save()
        
        newlisting = Listing(
            title = title,
            description = description,
            imageUrl = imageUrl,
            price = bid,
            category_listing = categoryData, 
            owner = currentUser,
        )
        newlisting.save()
        return  HttpResponseRedirect(reverse(index))
    
def displayCategory(request):
    categoryFromForm = request.POST['v1']
    t1 = category.objects.get(categoryName=categoryFromForm)
    activeListings = Listing.objects.filter(isActive=True , category_listing=t1)
    allCategories = category.objects.all()
    return render(request, "auctions/index.html",{
        "Listings": activeListings,
        "categories": allCategories,
    })


def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    allComment = Comment.objects.filter(listing=listingData)
    islistingInwatchlist = request.user in listingData.watchlist.all()
    isOwner = request.user.username == listingData.owner.username
    if listingData.isActive == False:
        if request.user == listingData.price.by_user:
            return render(request, "auctions/listing.html",{
            "listing":listingData,
            "islistingInwatchlist":islistingInwatchlist,
            "allComment":allComment,
            "isOwner":isOwner,
            "m1" : "You won the auction"
            })
    return render(request, "auctions/listing.html",{
        "listing":listingData,
        "islistingInwatchlist":islistingInwatchlist,
        "allComment":allComment,
        "isOwner":isOwner,
    })


def closeauction(request, id):
    listingData=Listing.objects.get(pk=id)
    listingData.isActive = False
    allComment = Comment.objects.filter(listing=listingData)
    islistingInwatchlist = request.user in listingData.watchlist.all()
    isOwner = request.user.username == listingData.owner.username
    listingData.save()
    return render(request, "auctions/listing.html",{
        "listing":listingData,
        "islistingInwatchlist":islistingInwatchlist,
        "allComment":allComment,
        "isOwner":isOwner,
        "updata":True,
        "message":"Congratulation!"
    })

def removewatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse(listing,args=(id, ))) 


def addwatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    
    return HttpResponseRedirect(reverse(listing,args=(id, )))


def watchlist(request):
    currentUser = request.user
    listing = currentUser.cart.all()
    return render(request, "auctions/watchlist.html",{
        "Listings": listing
    }) 


def addBid(request, id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    allComment = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    islistingInwatchlist = request.user in listingData.watchlist.all()
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(by_user=request.user, bid=int(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html",{
            "listing": listingData,
            "message": "Bid was updated successfully",
            "update": True,
            "islistingInwatchlist":islistingInwatchlist,
            "allComment":allComment,
            "isOwner":isOwner,
        })
    
    else:
         return render(request, "auctions/listing.html",{
            "listing": listingData,
            "message": "Bid Failed",
            "update": False,
            "islistingInwatchlist":islistingInwatchlist,
            "allComment":allComment,
            "isOwner":isOwner,
        })

def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']

    newComment= Comment(
        author=currentUser,
        listing= listingData,
        message= message,
     )
    
    newComment.save()
    return HttpResponseRedirect(reverse(listing,args=(id, )))