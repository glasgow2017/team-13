from django.shortcuts import render, HttpResponse, redirect
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.views import login
from .forms import ProfileForm
from .models import UserProfile, Request, User


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


def get_most_urgent_request(r_user):
    if r_user.is_authenticated() == False:
        return("NOT_LOGGED_IN")
    user = UserProfile.objects.get(id=r_user.id)
    if user.role==2:
        priority_list = Request.objects.filter(is_taken=False).order_by('-weight')
        if priority_list:
            return priority_list[0]
        # Return false if there are no outstanding requests
        return False
    else:
        return redirect('/accounts/login')


def responder_page(request):
    priority_req = get_most_urgent_request(request.user)
    if (priority_req == "NOT_LOGGED_IN"):
        return redirect('/accounts/login')
    if (priority_req):
        priority_user = priority_req.request_user
        return render(request, "responder_page.html", {"p_user": priority_user, "background": priority_user.get_background_display()})
    return render(request, "responder_page.html", {})


def about(request):
    return render(request, "about.html", {})


def links(request):
    return render(request, "links.html", {})