from django.shortcuts import render, HttpResponse
from django.db.models import ObjectDoesNotExist
from .forms import ProfileForm
from .models import UserProfile, Request


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


def get_most_urgent_request(user):
    user = UserProfile.objects.get(id=user.id)
    if user.role==2:
        priority_list = Request.objects.filter(is_taken=False).order_by('-weight')
        if priority_list:
            return priority_list[0]
        # Return false if there are no outstanding requests
        return False
    else:
        return HttpResponse('You are not a responder.')


def responder_page(request):
    priority_user = get_most_urgent_request(request.user)
    return render(request, "responder_page.html", {"user": priority_user})

