from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve

from . import views
app_name = "auctions"
urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # Serve static file
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path("", views.index, name="index"),
    path("list_items", views.ListItems.as_view(), name="list_items"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.CreatePost.as_view(), name="add_post"),
    path("<pk>", views.ItemDetailView.as_view(), name="item_detail"),
    path("<pk>/delete_item", views.ItemDeleteView.as_view(), name="delete_item"),
]
