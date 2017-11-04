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
    comments = models.CharField(max_length=1000, blank=True)
    dob = models.DateField(blank=False)
    gender = models.IntegerField(GENDER_CHOICES, blank=False)
    background = models.IntegerField(BACKGROUND_CHOICES, blank=False)
    previous_issues = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    registered_on = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name
