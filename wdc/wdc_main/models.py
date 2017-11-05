import math

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ADMIN_CHOICE = 1
    RESPONDER_CHOICE = 2
    USER_CHOICE = 3

    ROLE_CHOICES = (
        (ADMIN_CHOICE, "Admin"),
        (RESPONDER_CHOICE, "Responder"),
        (USER_CHOICE, "User")
    )

    ENGLAND_CHOICE = 0
    SCOTLAND_CHOICE = 1
    WALES_CHOICE = 2
    NI_CHOICE = 3

    REGION_CHOICES = (
        (ENGLAND_CHOICE, "England"),
        (SCOTLAND_CHOICE, "Scotland"),
        (WALES_CHOICE, "Wales"),
        (NI_CHOICE, "Northern Ireland")
    )

    FEMALE_CHOICE = 0
    MALE_CHOICE = 1
    OTHER_CHOICE = 2
    NOT_DISCLOSED_CHOICE = 3

    GENDER_CHOICES = (
        (FEMALE_CHOICE, "Female"),
        (MALE_CHOICE, "Male"),
        (OTHER_CHOICE, "Other"),
        (NOT_DISCLOSED_CHOICE, "Not Disclosed")
    )

    MILITARY_CHOICE = 0
    POLICE_CHOICE = 1
    FIRE_CHOICE = 2
    PRISON_CHOICE = 3
    NHS_CHOICE = 4
    OTHER_CHOICE = 5

    BACKGROUND_CHOICES = (
        (MILITARY_CHOICE, "Military"),
        (POLICE_CHOICE, "Police"),
        (FIRE_CHOICE, "Fire Service"),
        (PRISON_CHOICE, "Prison Staff"),
        (NHS_CHOICE, "NHS Staff"),
        (OTHER_CHOICE, "Other Background")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLE_CHOICES, default=USER_CHOICE)
    name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    region = models.IntegerField(choices=REGION_CHOICES, blank=True, null=True)
    comments = models.CharField(max_length=1000, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True)
    background = models.IntegerField(choices=BACKGROUND_CHOICES, blank=True, null=True)
    previous_issues = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    registered_on = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name


class Request(models.Model):
    EMERGENCY_CHOICE = 0
    HOUSING_CHOICE = 1
    JOB_CHOICE = 2
    LONELINESS_CHOICE = 3

    CATEGORY_CHOICES = (
        (EMERGENCY_CHOICE, 'Emergency'),
        (HOUSING_CHOICE, 'Housing'),
        (JOB_CHOICE, 'Job'),
        (LONELINESS_CHOICE, 'Loneliness')
    )

    CATEGORY_WEIGHTS = (500, 3, 2, 5)

    timestamp = models.DateTimeField(auto_now_add=timezone.now)
    category = models.IntegerField(choices=CATEGORY_CHOICES, blank=False)
    weight = models.IntegerField(blank=False, default=1)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_long = models.DecimalField(max_digits=9, decimal_places=6)
    request_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    responder = models.ManyToManyField(UserProfile, blank=True, related_name="responder")
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return self.request_user.name + str(self.id)

    def set_weight(self):
        """
        Calculates and saves the current weight of the request.
        This weight is the sum of:
        1.) The predefined weight corresponding to the category of the request.
        2.) A large value if the user requesting help has previous mental health issues
        3.) An exponentially growing value corresponding to the length this request has spent in the queue.
        """
        category_weight = self.CATEGORY_WEIGHTS[self.category]

        previous_issue_weight = 100 if self.request_user.previous_issues else 0

        time_weight = 0
        if (self.timestamp):
            time_weight = math.exp((timezone.now() - self.timestamp).total_seconds() / 1000)

        self.weight = category_weight + previous_issue_weight + time_weight

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.set_weight()
        super(Request, self).save(force_insert, force_update, using, update_fields)


class Call(models.Model):
    usr_rating = models.IntegerField(blank=True, null=True)
    responder_rating = models.IntegerField(blank=True, null=True)
    usr_comment = models.CharField(max_length=500, blank=True, null=True)
    responder_comment = models.CharField(max_length=500, blank=True, null=True)
    duration = models.DurationField(blank=False)
    resolved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=timezone.now)
    request = models.OneToOneField(Request, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
