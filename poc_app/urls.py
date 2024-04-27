from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("forms/", views.forms, name="forms"),
    path("get_couponcodes_json_paging/", views.get_couponcodes_json_paging, name="get_couponcodes_json_paging"),
    path("get_fields/", views.get_fields, name="get_fields"),
    path("save_custom_filter/", views.save_custom_filter, name="save_custom_filter")

]
