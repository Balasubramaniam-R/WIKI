from django.urls import path
from . import views

app_name= "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.get,name="get"),
    path("search",views.search,name="search"),
    path("create",views.add,name="add"),
    path("edit",views.edit,name="edit"),
    path("random",views.random,name="random")
]
