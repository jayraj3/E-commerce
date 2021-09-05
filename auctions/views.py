from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from .models import User, CreateAdd
from .forms import CreateAddForm


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        email_confirmation = request.POST['email_confirmation']

        # Ensure password matches confirmation
        password = request.POST["password"]
        password_confirmation = request.POST["password_confirmation"]
        if password != password_confirmation or email != email_confirmation:
            return render(request, "auctions/register.html", {
                "message": "Email or Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


class CreatePost(CreateView):
    model = CreateAdd
    form_class = CreateAddForm
    template_name = 'auctions/create_form.html'
    #success_url = reverse_lazy('auction:index')
    @method_decorator(login_required)
    def post(self, request):
        form = CreateAddForm(request.POST,request.FILES)
        #print(request.POST)
        if form.is_valid():
            user = request.user
            post = form.save(commit=False)
            post.user = user
            post.save()
        return render(request, "auctions/index.html")

