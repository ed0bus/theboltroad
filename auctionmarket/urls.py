from django.urls import path, include
from . import views
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls


urlpatterns = [
    path("auctionmarket", views.bid, name="auctionmarket"),
    path("signup", views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("vehicle/<int:pk>/", views.retrieve_info, name="retrieve_info"),
    path("profile", views.profile_info, name="profile_info"),
    path("", views.home, name="home"),
    path("auctions/<int:pk>/cancel_bid/", views.cancel_bid, name="cancel_bid"),
]
