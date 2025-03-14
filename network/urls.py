
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("handlelike/<str:entry_type>/<int:entry_id>", views.handlelike, name="handlelike"),
    path("delete/<str:entry_type>/<int:entry_id>", views.delete, name="delete"),
    path("edit/<str:entry_type>/<int:entry_id>", views.edit, name="edit"),
    path("handlefollow/<int:user_id>", views.handlefollow, name="handlefollow"),
    path("following", views.following, name="following"),
    path("update/<int:user_id>", views.update ,name="update"),
    path("users/<str:group>/<int:obj_id>", views.users, name="users"),
]
