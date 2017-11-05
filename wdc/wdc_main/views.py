from django.shortcuts import render
from django.db.models import ObjectDoesNotExist
from .forms import ProfileForm
from .models import UserProfile


def index(request):
    return render(request, "index.html", {"welcome": "hello"})


def profile(request):
    if request.user.is_authenticated():
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=request.user)

        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
        else:
            try:
                form = ProfileForm(instance=UserProfile.objects.get(user=request.user))
            except ObjectDoesNotExist:
                form = ProfileForm()


        return render(request, "profile.html", {"form": form})

    return render(request, "profile.html", {})
