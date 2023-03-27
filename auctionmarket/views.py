from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import (
    Auction,
    Customer,
    AuctionOutcome,
    Bicycle,
    Scooter,
    Skateboard,
    Hoverboard,
)
from django.core.cache import cache
import time
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages


def bid(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        current_user = request.user
        customer = Customer.objects.get(user=current_user)
        balance = customer.balance
        print(balance)
        # aste = Auction.objects.all()
        aste = Auction.objects.filter(
            auction_endtime__gte=datetime.fromtimestamp(time.time())
        )
        # aggiungi minimum offer must be higher
        if request.method == "POST":
            try:
                bid_value = float(request.POST["bid"])
                print(bid_value)
                # update cache data
                auction_id = request.POST["auction_id"]
                selected = Auction.objects.get(pk=auction_id)
                if bid_value < selected.minimum_bid:
                    messages.warning(request, "Your bid is not high enough!")
                elif selected.auction_endtime.timestamp() < time.time():
                    print("the auction is already ended!")
                    return HttpResponse("Auction has already ended!")
                #
                else:
                    hash_key = str(selected.pk)
                    # if is the first bid ever on the auction create a new cache object
                    if cache.get(hash_key) == None:
                        highest_bid = float(bid_value)

                        hash_value = {
                            "highest_bid": highest_bid,
                            "highest_bidder": current_user,
                        }
                        # auction_duration = expiration_time - time.time() + 100
                        cache.add(hash_key, hash_value)
                        new_balance = balance - bid_value
                        customer.balance = new_balance
                        customer.save()

                    # set the hash key

                    else:
                        if bid_value <= cache.get(str(selected.pk))["highest_bid"]:
                            messages.warning(request, "Your bid is not high enough!")
                        else:
                            hash_value = cache.get(hash_key)
                            previous = hash_value["highest_bidder"]
                            print(previous)
                            print(customer.user)
                            if previous is not None and previous != customer.user:
                                previous_customer = Customer.objects.get(user=previous)
                                previous_customer.balance += hash_value["highest_bid"]
                                previous_customer.save()
                            elif previous == customer.user:
                                print("equal to customer")
                                print(hash_value["highest_bid"])
                                customer.balance = balance + hash_value["highest_bid"]

                            new_balance = customer.balance - bid_value
                            customer.balance = new_balance
                            customer.save()
                            # if the hash key exist you have to check
                            hash_value["highest_bid"] = float(bid_value)
                            hash_value["highest_bidder"] = current_user
                            cache.set(hash_key, hash_value)

                    print(cache.get(hash_key))
            # create a dictionary mapping auction IDs to highest bid values
            except:
                messages.warning(
                    request, "Empty or not numeric values are not accepted!!"
                )
        context = {"auctions": aste}
        return render(request, "auctionmarket.html", context)
    else:
        try:
            aste = Auction.objects.filter(
                auction_endtime__gte=datetime.fromtimestamp(time.time())
            )
            if request.method == "POST" and request.user.is_superuser:
                messages.warning(
                    request, "Since you are an admin you are unable to place a bid!!"
                )
            elif request.method == "POST":
                messages.warning(
                    request, "You have to login first if you want to place a bid!"
                )

            return render(
                request,
                "auctionmarket.html",
                {"auctions": aste},
            )
        except:
            return render(request, "auctionmarket.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password1 = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password1)
            Customer.objects.create(user=user, balance=100000.0)
            login(request, user)
            return redirect(bid)
        else:
            return render(request, "signup.html", {"form": form})
    else:
        form = UserCreationForm()
        return render(request, "signup.html", {"form": form})


def retrieve_info(request, pk):
    auction = Auction.objects.get(pk=pk)
    if auction.bicycle is not None:
        bicycle = Bicycle.objects.get(pk=auction.bicycle.pk)
        return render(request, "bicycle.html", {"bicycle": bicycle})
    elif auction.scooter is not None:
        scooter = Scooter.objects.get(pk=auction.scooter.pk)
        return render(request, "scooter.html", {"scooter": scooter})
    elif auction.skateboard is not None:
        skateboard = Skateboard.objects.get(pk=auction.skateboard.pk)
        return render(request, "skateboard.html", {"skateboard": skateboard})
    elif auction.hoverboard is not None:
        hoverboard = Hoverboard.objects.get(pk=auction.hoverboard.pk)
        return render(request, "hoverboard.html", {"hoverboard": hoverboard})
    else:
        return HttpResponse("Vehicle not found.")


def profile_info(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        current_user = request.user

        customer = Customer.objects.get(user=current_user)
        won_auctions = AuctionOutcome.objects.filter(winner=current_user)
        return render(
            request,
            "profile.html",
            {"won_auctions": won_auctions, "customer": customer},
        )
    else:
        return render(request, "profile.html")


def home(request):
    try:
        values = [x.highest_bid for x in AuctionOutcome.objects.all()]
        total = sum(values)
        print(total)
        return render(request, "home.html", {"total": total})
    except:
        return render(request, "home.html")


def cancel_bid(request, pk):
    auction_data = cache.get(str(pk))
    if auction_data is not None and auction_data["highest_bidder"] == request.user:
        returned_amount = auction_data["highest_bid"]
        customer = Customer.objects.get(user=request.user)
        customer.balance = customer.balance + returned_amount
        customer.save()
        auction_data["highest_bid"] = 0
        auction_data["highest_bidder"] = None
        cache.set(str(pk), auction_data)
    return redirect("auctionmarket")
