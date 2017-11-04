from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    ENGLAND_CHOICE = 1
    SCOTLAND_CHOICE = 2
    WALES_CHOICE = 3
    NI_CHOICE = 4

    REGION_CHOICES = (
        (ENGLAND_CHOICE, "England"),
        (SCOTLAND_CHOICE, "Scotland"),
        (WALES_CHOICE, "Wales"),
        (NI_CHOICE, "Northern Ireland")
    )

    FEMALE_CHOICE = 1
    MALE_CHOICE = 2
    OTHER_CHOICE = 3
    NOT_DISCLOSED_CHOICE = 4

    GENDER_CHOICES = (
        (FEMALE_CHOICE, "Female"),
        (MALE_CHOICE, "Male"),
        (OTHER_CHOICE, "Other"),
        (NOT_DISCLOSED_CHOICE, "Not Disclosed")
    )

    MILITARY_CHOICE = 1
    POLICE_CHOICE = 2
    FIRE_CHOICE = 3
    PRISON_CHOICE = 4
    NHS_CHOICE = 5
    OTHER_CHOICE = 6

    BACKGROUND_CHOICES = (
        (MILITARY_CHOICE, "Military"),
        (POLICE_CHOICE, "Police"),
        (FIRE_CHOICE, "Fire Service"),
        (PRISON_CHOICE, "Prison Staff"),
        (NHS_CHOICE, "NHS Staff"),
        (OTHER_CHOICE, "Other Background")
    )

    name = models.CharField(max_length=255, blank=False)
    telephone = models.CharField(max_length=20, blank=False)
    region = models.IntegerField(choices=REGION_CHOICES, blank=False)
    comments = models.CharField(max_length=1000, blank=True, null=True)
    dob = models.DateField(blank=False)
    gender = models.IntegerField(GENDER_CHOICES, blank=False)
    background = models.IntegerField(BACKGROUND_CHOICES, blank=False)
    previous_issues = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    registered_on = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name


class Request(models.Model):
    EMERGENCY_CHOICE = 1
    HOUSING_CHOICE = 2
    JOB_CHOICE = 3
    LONELINESS_CHOICE = 4

    CATEGORY_CHOICES = (
        (EMERGENCY_CHOICE, 'Emergency'),
        (HOUSING_CHOICE, 'Housing'),
        (JOB_CHOICE, 'Job'),
        (LONELINESS_CHOICE, 'Loneliness')
    )

    timestamp = models.DateTimeField(auto_now_add=timezone.now)
    category = models.IntegerField(choices=CATEGORY_CHOICES, blank=False)
    weight = models.IntegerField(blank=False, default=1)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_long = models.DecimalField(max_digits=9, decimal_places=6)
    request_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE(), on_update=models.CASCADE())
    responder = models.ManyToManyField(UserProfile, on_delete=models.CASCADE(), on_update=models.CASCADE(), blank=True, null=True)

class Call(models.Model):
    usr_rating = models.IntegerField(blank=True, null=True)
    responder_rating = models.IntegerField(blank=True, null=True)
    usr_comment = models.CharField(max_length=500, blank=True, null=True)
    responder_comment = models.CharField(max_length=500, blank=True, null=True)
    duration = models.DurationField(blank=False)
    resolved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=timezone.now)
    request = models.OneToOneField(Request, on_delete=models.CASCADE(), on_update=models.CASCADE())
