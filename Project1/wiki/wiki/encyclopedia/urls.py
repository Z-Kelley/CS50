from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.title, name="title"),
    path("create/", views.createNew, name="createnew"),
    path("random/", views.randomPage, name="randomPage"),
    path("wiki/<str:entry>/edit", views.editPage, name="editPage"),
    path("searchresults/", views.searchResults, name="searchResults"),
    path("saveEdit/", views.saveEdit, name="saveEdit")
]
