from celery import shared_task
from django.utils import timezone
from .models import Auction, AuctionOutcome
from django.core.cache import cache
import json
from .utils import sendTransaction
import hashlib
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.core.files.base import ContentFile


@shared_task(name="monitor_auctions")
def monitor_auctions():
    # filter expired auctions not yet marked as ended
    aste = Auction.objects.filter(auction_endtime__lt=timezone.now(), ended=False)
    outcomes = []
    for auction in aste:
        hash_key = str(auction.pk)  # always convert pk to a str
        # check if there is an object in the cache with existing pk
        hash_value = cache.get(hash_key)
        if hash_value is not None and hash_value["highest_bid"] > 0:
            # register and save the outcome
            outcome = AuctionOutcome(
                auction=auction,
                winner=hash_value["highest_bidder"],
                highest_bid=hash_value["highest_bid"],
            )
            cache.delete(hash_key)
            auction.ended = True
            auction.save()
            # update the status of the sold vehicle
            if auction.bicycle is not None:
                auction.bicycle.sold = True
                auction.bicycle.in_auction = False
                auction.bicycle.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "bicycle",
                    ],
                )
            elif auction.scooter is not None:
                auction.scooter.sold = True
                auction.scooter.in_auction = False
                auction.scooter.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "scooter",
                    ],
                )
            elif auction.hoverboard is not None:
                auction.hoverboard.in_auction = False
                auction.hoverboard.sold = True
                auction.hoverboard.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "hoverboard",
                    ],
                )
            elif auction.skateboard is not None:
                auction.skateboard.in_auction = False
                auction.skateboard.sold = True
                auction.skateboard.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "skateboard",
                    ],
                )

            # convert necessary informations to dict and dump thems in a json
            outcome_data = model_to_dict(
                outcome, exclude=["id", "json_downloadable", "tx_id", "hashed_json"]
            )
            outcome_data["auction"] = auction_data
            outcome_data["winner"] = outcome.winner.username
            print(outcome_data)
            json_file = json.dumps(outcome_data, indent=1, cls=DjangoJSONEncoder)
            # hash the json
            json_hash = hashlib.sha256(json_file.encode("utf-8")).hexdigest()
            print(json_hash)
            outcome.hashed_json = json_hash
            # send transaction to goerli blockchain
            tx_id = sendTransaction(json_hash)
            print(tx_id)
            outcome.tx_id = str(tx_id)
            outcome.json_downloadable.save(
                f"{auction.pk}_outcome.json", ContentFile(json_file)
            )
            outcomes.append(outcome)
            outcome.save()
        # the auction object is in the cache but the highest bid is zero
        elif hash_value is not None and hash_value["highest_bid"] == 0:
            auction.ended = True
            auction.save()
            if auction.bicycle is not None:
                auction.bicycle.sold = False
                auction.bicycle.in_auction = False
                auction.bicycle.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "bicycle",
                    ],
                )
            elif auction.scooter is not None:
                auction.scooter.sold = False
                auction.scooter.in_auction = False
                auction.scooter.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "scooter",
                    ],
                )
            elif auction.hoverboard is not None:
                auction.hoverboard.in_auction = False
                auction.hoverboard.sold = False
                auction.hoverboard.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "hoverboard",
                    ],
                )
            elif auction.skateboard is not None:
                auction.skateboard.in_auction = False
                auction.skateboard.sold = False
                auction.skateboard.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "skateboard",
                    ],
                )
            # what happen if the transaction has no offers? or there is an auction but the offer is zero

            # rember that if a user cancel the bid the highest bidder will be none and highest bid will be zero but the key will exist in the redis database
        else:
            auction.ended = True
            auction.save()
            if auction.bicycle is not None:
                auction.bicycle.sold = False
                auction.bicycle.in_auction = False
                auction.bicycle.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "bicycle",
                    ],
                )
            elif auction.scooter is not None:
                auction.scooter.sold = False
                auction.scooter.in_auction = False
                auction.scooter.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "scooter",
                    ],
                )
            elif auction.hoverboard is not None:
                auction.hoverboard.in_auction = False
                auction.hoverboard.sold = False
                auction.hoverboard.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "hoverboard",
                    ],
                )
            elif auction.skateboard is not None:
                auction.skateboard.in_auction = False
                auction.skateboard.sold = False
                auction.skateboard.save()
                auction_data = model_to_dict(
                    outcome.auction,
                    fields=[
                        "id",
                        "minimum_bid",
                        "auction_endtime",
                        "ended",
                        "skateboard",
                    ],
                )
