from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", login_required(TemplateView.as_view(template_name="index.html")), name="index"),
    path("index/", login_required(TemplateView.as_view(template_name="index.html")), name="index"),
    path("login/", views.login, name="login"),
    path("login/submit", views.submit_login, name="submit_login"),
    path("logout/", views.logout, name="logout"),
]
