from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('organization', views.show_all),
    path("organization/create", views.create_organization),
    path("organization/<int:id>", views.one_org),
    path("organization/<int:id>/delete", views.delete),
    path("join/<int:id>", views.join_org),
    path("leave/<int:id>", views.leave_org),
    path("logout", views.logout)
]