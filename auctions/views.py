from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import create_listings
from .models import User,auction_listing,category,WatchList,Bid,Comments
x=0
def index(request):
    return render(request,"auctions/index.html",{
        "lists":auction_listing.objects.all()
    })

def login_view(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"auctions/login.html",{
                "message":"Invalid Credentials."
            })
    else:
        return render(request,"auctions/login.html")

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

def create(request):

    if request.method=="POST":
       name=request.POST["name"]
       price=request.POST["price"]
       creation_date=request.POST["creation_date"]
       images=request.POST["images"]
       category=request.POST["categories"]
       curr=price
       forms=auction_listing(name=name,price=price,creation_date=creation_date,images=images,user=request.user,categories_id=category)

       forms.save()
       form=Bid(name=forms,bid=curr,user=request.user)


       form.save()
       return HttpResponseRedirect(reverse("index"))

    return render(request,"auctions/create.html",{
        "form":create_listings()
    })
def listing(request,id):
    if request.method=="POST":
        if 'comm_sub' in request.POST:
            abc=auction_listing.objects.get(id=id)
            comment=request.POST["content"]
            forms=Comments(comm_name=abc,content=comment,user=request.user)
            forms.save()
            return HttpResponseRedirect(reverse("listing",args=(id,)))
        if 'close_sub' in request.POST:
            abc=auction_listing.objects.get(id=id)
            abc.close="Close"
            abc.save()
            return HttpResponseRedirect(reverse("listing",args=(id,)))
        if 'bid_sub' in request.POST:
            auc=auction_listing.objects.get(id=id)

            if request.user!= auc.user:
                bid=request.POST["bid"]
                bid=float(bid)
                bids=Bid.objects.all().get(name=auc)
            else:
                return HttpResponse("You are the owner why are you bidding?")
            if bid>bids.bid:
                forms=Bid(name=auc,bid=bid,user=request.user)
                forms.save(update_fields=['bid','user'])
                return HttpResponseRedirect(reverse("listing",args=(id,)))
            else:
                return HttpResponse("Bid cannot be lower than current price")
            

    abc=auction_listing.objects.get(id=id)
    print(abc)
    bid=Bid.objects.get(name=abc)
    print(bid)
    cats=category.objects.get(pk=abc.categories_id)
    return render(request,"auctions/listings.html",{
        "lists":auction_listing.objects.get(id=id),
        "cat":  cats,
        "bids":bid,
        "comments":Comments.objects.all(),
        "userr":request.user


    })
def watchlist(request):
    auc=WatchList.objects.all().filter(user=request.user)
    return render(request,"auctions/watchlist.html",{
        "auc":auc
    })


def categories(request):
    return render(request,"auctions/category.html",{
        "lists": category.objects.all()
    })
def category_id(request,ids):
    cats=category.objects.get(pk=ids)

    return render(request,"auctions/category_id.html",{
        "lists":  cats.cat.values('name','id'),

    })
def add(request,id):
    auc=auction_listing.objects.get(id=id)

    forms=WatchList(watch_name=auc,user=request.user)

    forms.save()
    wat=WatchList.objects.all().filter(user=request.user)
    return HttpResponseRedirect(reverse("watchlist"))
