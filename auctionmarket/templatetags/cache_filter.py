from django import template
from django.core.cache import cache


register = template.Library()


@register.filter
def hb_value(primary_key):
    hashkey = cache.get(primary_key)
    if hashkey is not None:
        hash_value = hashkey["highest_bid"]
        return hash_value
    else:
        return 0


@register.filter
def fetch_hbidder(pk):
    hashkey = cache.get(pk)
    if hashkey is not None:
        highest_bidder = hashkey["highest_bidder"]
        return highest_bidder
    else:
        return None
