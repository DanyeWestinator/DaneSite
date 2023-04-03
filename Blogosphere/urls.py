from django.urls import path
#import the local views
from . import views


#global vars
urlpatterns = [
    path("", views.Homepage, name="index"),
    path("Index", views.Homepage, name="index"),
    path("Blogosphere", views.BlogosphereHome, name="index"),
    path(r"<int:id>/", views.entry, name = "entry"),
    path(r"Portfolio/<str:type>/", views.Portfolio, name="index")
]