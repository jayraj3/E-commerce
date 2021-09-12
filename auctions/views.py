from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from .models import User, Item
from .forms import ItemForm


def index(request):
    return HttpResponseRedirect(reverse("auctions:list_items"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:list_items"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:list_items"))


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
        return HttpResponseRedirect(reverse("auctions:list_items"))
    else:
        return render(request, "auctions/register.html")


class CreatePost(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'auctions/create_form.html'

    @method_decorator(login_required)
    def post(self, request):
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            post = form.save(commit=False)
            post.user = user
            post.save()
        return HttpResponseRedirect(reverse("auctions:list_items"))


class ListItems(ListView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ItemDetailView(DetailView):
    model = Item


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    login_url = reverse_lazy('auctions:login')
    success_url = reverse_lazy('auctions:list_items')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(ItemDeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj
