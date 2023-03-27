from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

# asta creata dall'amministratore per vendere mezzi elettrici
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=500000.0)


class Bicycle(models.Model):
    FRAME_MATERIAL_CHOICES = (
        ("Aluminum", "Aluminum"),
        ("Carbon Fiber", "Carbon Fiber"),
        ("Steel", "Steel"),
    )
    WHEEL_SIZE_CHOICES = (
        ("700C", "622mm"),
        ("650C", "571mm"),
        ("650B", "584mm"),
        ("650A", "590mm"),
    )

    SUSPENSION_TYPE_CHOICES = [
        ("front", "Front Suspension"),
        ("full", "Full Suspension"),
        ("rigid", "Rigid"),
        ("seatpost", "Suspension Seatpost"),
        ("soft-tail", "Soft-Tail"),
        ("dual", "Dual Suspension"),
    ]

    BATTERY_CAPACITY_CHOICES = [
        (350, "350 Wh"),
        (500, "500 Wh"),
        (700, "700 Wh"),
    ]

    MOTOR_POWER_CHOICES = [
        (0.25, "250W"),
        (0.5, "500W"),
        (0.75, "750W"),
        (1.0, "1000W"),
        (1.5, "1500W"),
        (2.0, "2000W"),
    ]
    model_name = models.CharField(max_length=60, default=None)
    description = models.CharField(max_length=1000, default=None)
    frame_material = models.CharField(max_length=15, choices=FRAME_MATERIAL_CHOICES)
    wheel_size = models.CharField(max_length=4, choices=WHEEL_SIZE_CHOICES)
    suspension_type = models.CharField(max_length=10, choices=SUSPENSION_TYPE_CHOICES)
    battery_capacity = models.IntegerField(choices=BATTERY_CAPACITY_CHOICES)
    motor_power = models.DecimalField(
        max_digits=6, decimal_places=2, choices=MOTOR_POWER_CHOICES
    )
    MAX_SPEED_KMH = 65
    maximum_speed_kmh = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MaxValueValidator(MAX_SPEED_KMH)]
    )
    MAX_DISTANCE_KM = 80

    max_distance_km = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MaxValueValidator(MAX_DISTANCE_KM)]
    )
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    foldable = models.BooleanField()
    vehicle_pic = models.ImageField(upload_to="images", default=None)
    in_auction = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.model_name}"


# correggi
class Scooter(models.Model):
    FRAME_MATERIAL_CHOICES = (
        ("Aluminum", "Aluminum"),
        ("Carbon Fiber", "Carbon Fiber"),
        ("Steel", "Steel"),
    )

    WHEEL_SIZE_CHOICES = (
        ("8", "8 inch"),
        ("10", "10 inch"),
        ("12", "12 inch"),
        ("14", "14 inch"),
    )

    SUSPENSION_TYPE_CHOICES = (
        ("front", "Front Suspension"),
        ("rear", "Rear Suspension"),
        ("dual", "Dual Suspension"),
        ("none", "No Suspension"),
    )

    BATTERY_CAPACITY_CHOICES = (
        (350, "350 Wh"),
        (500, "500 Wh"),
        (700, "700 Wh"),
        (1000, "1000 Wh"),
    )

    MOTOR_POWER_CHOICES = (
        (250, "250W"),
        (500, "500W"),
        (750, "750W"),
        (1000, "1000W"),
    )
    model_name = models.CharField(max_length=60, default=None)
    description = models.CharField(max_length=1000, default=None)
    frame_material = models.CharField(max_length=15, choices=FRAME_MATERIAL_CHOICES)
    wheel_size = models.CharField(max_length=2, choices=WHEEL_SIZE_CHOICES)
    suspension_type = models.CharField(max_length=5, choices=SUSPENSION_TYPE_CHOICES)
    battery_capacity = models.IntegerField(choices=BATTERY_CAPACITY_CHOICES)
    motor_power = models.IntegerField(choices=MOTOR_POWER_CHOICES)

    MAX_SPEED_KMH = 45
    maximum_speed_kmh = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MaxValueValidator(MAX_SPEED_KMH)]
    )

    MAX_DISTANCE_KM = 80
    max_distance_km = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MaxValueValidator(MAX_DISTANCE_KM)]
    )

    weight = models.DecimalField(max_digits=6, decimal_places=2)
    foldable = models.BooleanField()

    vehicle_pic = models.ImageField(upload_to="images", default=None)
    in_auction = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.model_name}"


class Skateboard(models.Model):
    DECK_MATERIAL_CHOICES = (
        ("Wood", "Wood"),
        ("Plastic", "Plastic"),
        ("Carbon Fiber", "Carbon Fiber"),
    )

    DECK_LENGTH_CHOICES = (
        (28, "28 inches"),
        (32, "32 inches"),
        (36, "36 inches"),
    )

    TRUCK_TYPE_CHOICES = (
        ("standard", "Standard"),
        ("reverse kingpin", "Reverse Kingpin"),
        ("traditional kingpin", "Traditional Kingpin"),
    )

    WHEEL_SIZE_CHOICES = (
        (52, "52 mm"),
        (54, "54 mm"),
        (56, "56 mm"),
        (58, "58 mm"),
    )

    WHEEL_HARDNESS_CHOICES = (
        ("soft", "Soft"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    )

    DECK_MATERIAL_CHOICES = (
        ("WD", "Wood"),
        ("PL", "Plastic"),
        ("CF", "Carbon Fiber"),
    )

    BATTERY_CAPACITY_CHOICES = [
        (99, "99 Wh"),
        (160, "160 Wh"),
        (260, "260 Wh"),
        (360, "360 Wh"),
        (500, "500 Wh"),
        (720, "720 Wh"),
    ]
    MOTOR_POWER_CHOICES = [
        (250, "250 W"),
        (350, "350 W"),
        (500, "500 W"),
        (1000, "1000 W"),
    ]

    model_name = models.CharField(max_length=60, default=None)
    description = models.CharField(max_length=1000, default=None)
    deck_material = models.CharField(max_length=2, choices=DECK_MATERIAL_CHOICES)
    deck_length = models.IntegerField(choices=DECK_LENGTH_CHOICES)
    truck_type = models.CharField(max_length=50, choices=TRUCK_TYPE_CHOICES)
    wheel_size = models.IntegerField(choices=WHEEL_SIZE_CHOICES)
    wheel_hardness = models.CharField(max_length=50, choices=WHEEL_HARDNESS_CHOICES)
    battery_capacity = models.IntegerField(choices=BATTERY_CAPACITY_CHOICES)
    motor_power = models.IntegerField(choices=MOTOR_POWER_CHOICES)
    MAX_SPEED_KMH = 30
    maximum_speed_kmh = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MaxValueValidator(MAX_SPEED_KMH)]
    )
    MAX_RANGE_KM = 30
    max_distance_km = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MaxValueValidator(MAX_RANGE_KM)]
    )
    weight = models.DecimalField(max_digits=6, decimal_places=2)

    vehicle_pic = models.ImageField(upload_to="images", default=None)
    in_auction = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.model_name}"


class Hoverboard(models.Model):
    WHEEL_SIZE_CHOICES = (
        (6.5, "6.5 inches"),
        (8.0, "8.0 inches"),
        (10.0, "10.0 inches"),
    )
    BATTERY_CAPACITY_CHOICES = [
        (54, "54 Wh"),
        (158, "158 Wh"),
        (220, "220 Wh"),
        (320, "320 Wh"),
        (430, "430 Wh"),
        (580, "580 Wh"),
    ]

    MOTOR_POWER_CHOICES = [
        (250, "250 W"),
        (350, "350 W"),
        (500, "500 W"),
        (1000, "1000 W"),
    ]

    model_name = models.CharField(max_length=60, default=None)
    description = models.CharField(max_length=1000, default=None)
    wheel_size = models.DecimalField(
        max_digits=3, decimal_places=1, choices=WHEEL_SIZE_CHOICES
    )
    battery_capacity = models.IntegerField(choices=BATTERY_CAPACITY_CHOICES)
    motor_power = models.IntegerField(choices=MOTOR_POWER_CHOICES)

    MAX_SPEED_KMH = 25  # set your maximum speed in MPH

    maximum_speed_kmh = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MaxValueValidator(MAX_SPEED_KMH)]
    )
    MAX_DISTANCE_KM = 15
    max_distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MaxValueValidator(MAX_DISTANCE_KM)],
    )
    weight = models.DecimalField(max_digits=6, decimal_places=2)

    vehicle_pic = models.ImageField(upload_to="images", default=None)
    in_auction = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"Hoverboard ({self.wheel_size} inch wheels)"


class Auction(models.Model):
    minimum_bid = models.FloatField()
    auction_endtime = models.DateTimeField()
    ended = models.BooleanField(default=False)

    bicycle = models.ForeignKey(
        Bicycle, on_delete=models.CASCADE, null=True, blank=True
    )
    scooter = models.ForeignKey(
        Scooter, on_delete=models.CASCADE, null=True, blank=True
    )
    skateboard = models.ForeignKey(
        Skateboard, on_delete=models.CASCADE, null=True, blank=True
    )
    hoverboard = models.ForeignKey(
        Hoverboard, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"Auction  with minimum bid of {self.minimum_bid}"

    def clean(self):
        if (
            sum(
                [
                    self.bicycle is not None,
                    self.scooter is not None,
                    self.skateboard is not None,
                    self.hoverboard is not None,
                ]
            )
            > 1
        ):
            raise ValidationError(
                "An auction instance can only be associated with one vehicle type."
            )


class AuctionOutcome(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.SET_NULL, null=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    highest_bid = models.FloatField()
    json_downloadable = models.FileField(upload_to="json", null=True, blank=True)
    hashed_json = models.CharField(max_length=64, null=True, blank=True)
    tx_id = models.CharField(max_length=100, null=True, blank=True)
