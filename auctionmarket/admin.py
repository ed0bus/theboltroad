from django.contrib import admin
from .models import (
    Auction,
    AuctionOutcome,
    Customer,
    Bicycle,
    Scooter,
    Skateboard,
    Hoverboard,
)


class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "minimum_bid", "auction_endtime", "ended")

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False  # disable editing for existing objects
        return super().has_change_permission(request, obj)

    # when you create an auction in the admin panel, select only not sold/not in auction items
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["bicycle", "scooter", "skateboard", "hoverboard"]:
            kwargs["queryset"] = db_field.related_model.objects.filter(
                sold=False, in_auction=False
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # on auction item is now being auction, so let's override the save method
    def save_model(self, request, obj, form, change):
        if obj.bicycle is not None:
            obj.bicycle.in_auction = True
            obj.bicycle.save()
        elif obj.scooter is not None:
            obj.scooter.in_auction = True
            obj.scooter.save()
        elif obj.skateboard is not None:
            obj.skateboard.in_auction = True
            obj.skateboard.save()
        elif obj.hoverboard is not None:
            obj.hoverboard.in_auction = True
            obj.hoverboard.save()
        super().save_model(request, obj, form, change)


class AuctionOutcomeAdmin(admin.ModelAdmin):
    # disable editing for existing auction and auction outcomes
    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj)

    list_display = ("auction", "winner", "highest_bid")


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")


class BicycleAdmin(admin.ModelAdmin):
    list_display = (
        "model_name",
        "frame_material",
        "wheel_size",
        "suspension_type",
        "battery_capacity",
        "motor_power",
        "max_distance_km",
        "vehicle_pic",
    )


class HoverboardAdmin(admin.ModelAdmin):
    list_display = (
        "model_name",
        "wheel_size",
        "battery_capacity",
        "motor_power",
        "max_distance_km",
        "maximum_speed_kmh",
        "weight",
        "vehicle_pic",
    )


class SkateboardAdmin(admin.ModelAdmin):
    list_display = (
        "model_name",
        "deck_material",
        "truck_type",
        "wheel_size",
        "wheel_hardness",
        "battery_capacity",
        "motor_power",
        "max_distance_km",
        "weight",
        "vehicle_pic",
    )


class ScooterAdmin(admin.ModelAdmin):
    list_display = (
        "model_name",
        "frame_material",
        "wheel_size",
        "suspension_type",
        "battery_capacity",
        "motor_power",
        "max_distance_km",
        "vehicle_pic",
    )


admin.site.register(Auction, AuctionAdmin)
admin.site.register(AuctionOutcome, AuctionOutcomeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Bicycle, BicycleAdmin)
admin.site.register(Skateboard, SkateboardAdmin)
admin.site.register(Hoverboard, HoverboardAdmin)
admin.site.register(Scooter, ScooterAdmin)
